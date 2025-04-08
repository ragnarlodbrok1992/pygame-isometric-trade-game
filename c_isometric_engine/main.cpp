#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#define SDL_MAIN_USE_CALLBACKS 1
#include <SDL3/SDL.h>
#include <SDL3/SDL_main.h>

#include "directx/d3d12.h"
#include "directx/d3dx12.h"
#include "directx/d3dcommon.h"
#include <dxgi1_6.h>
#include <d3dcompiler.h>

#include <stdio.h>
#include <wrl.h>

#include <string>
#include <codecvt>

// Compile defines
#define _DEBUG

static SDL_Window* window = nullptr;
static SDL_Renderer* renderer = nullptr;

// Engine variables
static UINT m_width = 1280;
static UINT m_height = 720;
static float m_aspectRatio = static_cast<float>(m_width) / static_cast<float>(m_height);
static std::wstring title = L"SDL Isometric Trade Game";
static std::wstring version = L"alpha";
static std::wstring identifier = L"ragnar.engine.ISOMETRIC";
static std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;

// DirectX3D variables
#define FRAME_COUNT 2
#define _DEBUG
static bool m_useWarpDevice = false; // WARP stands for Windows Advanced Rasterization Platform - software renderer, basically
                                     //
// Pipeline objects
D3D12_VIEWPORT m_viewport;
D3D12_RECT     m_scissorRect;
Microsoft::WRL::ComPtr<IDXGISwapChain3> m_swapChain;
Microsoft::WRL::ComPtr<ID3D12Device> m_device;
Microsoft::WRL::ComPtr<ID3D12Resource> m_renderTargets[FRAME_COUNT];
Microsoft::WRL::ComPtr<ID3D12CommandAllocator> m_commandAllocator;
Microsoft::WRL::ComPtr<ID3D12CommandQueue> m_commandQueue;
Microsoft::WRL::ComPtr<ID3D12RootSignature> m_rootSignature;
Microsoft::WRL::ComPtr<ID3D12DescriptorHeap> m_rtvHeap;
Microsoft::WRL::ComPtr<ID3D12PipelineState> m_pipelineState;
Microsoft::WRL::ComPtr<ID3D12GraphicsCommandList> m_commandList;
UINT m_rtvDescriptorSize;

// Application resources
Microsoft::WRL::ComPtr<ID3D12Resource> m_vertexBuffer;
D3D12_VERTEX_BUFFER_VIEW m_vertexBufferView;

// Synchronization objects
UINT m_frameIndex;
HANDLE m_fenceEvent;
Microsoft::WRL::ComPtr<ID3D12Fence> m_fence;
UINT64 m_fenceValue;

// Helper functions for C-->C++ interoperability by Microsoft
inline void ThrowIfFailed(HRESULT hr) {
  if (FAILED(hr)) {
    throw std::runtime_error("Failed HRESULT");
  }
}

// Helper function - getting hardware adapter
void GetHardwareAdapter(IDXGIFactory4* pFactory, IDXGIAdapter1** ppAdapter) {
  *ppAdapter = nullptr;
  for (UINT adapterIndex = 0; ; ++adapterIndex) {
      IDXGIAdapter1* pAdapter = nullptr;
      if (DXGI_ERROR_NOT_FOUND == pFactory->EnumAdapters1(adapterIndex, &pAdapter)) {
          // No more adapters to enumerate.
          break;
      } 

      // Check to see if the adapter supports Direct3D 12, but don't create the
      // actual device yet.
      if (SUCCEEDED(D3D12CreateDevice(pAdapter, D3D_FEATURE_LEVEL_11_0, _uuidof(ID3D12Device), nullptr))) {
          *ppAdapter = pAdapter;
          return;
      }
      pAdapter->Release();
  }
}

SDL_AppResult SDL_AppInit(void** appstate, int argc, char* argv[]) {
  // SDL_SetAppMetadata("SDL Isometric Trade Game", "alpha", "ragnar.engine.ISOMETRIC");
  // SDL_SetAppMetadata(static_cast<const char*>(title),
  //     static_cast<const char*>(version),
  //     static_cast<const char*>(identifier));
  // SDL_SetAppMetadata(title.c_str(), version.c_str(), identifier.c_str());
  SDL_SetAppMetadata(converter.to_bytes(title).c_str(),
      converter.to_bytes(version).c_str(),
      converter.to_bytes(identifier).c_str());

  if (!SDL_Init(SDL_INIT_VIDEO)) {
    SDL_Log("Couldn't initialize SDL: %s", SDL_GetError());
    return SDL_APP_FAILURE;
  }

  if (!SDL_CreateWindowAndRenderer("SDL Isometric Trade Game",
        m_width, m_height,
        0, &window, &renderer)) {
    SDL_Log("Couldn't create window/renderer: %s", SDL_GetError());
    return SDL_APP_FAILURE;
  }

  // Creating a handle to DirectX3D12

  HWND hwnd = (HWND) SDL_GetPointerProperty(SDL_GetWindowProperties(window),
      SDL_PROP_WINDOW_WIN32_HWND_POINTER, NULL);
  if (hwnd) {
    SDL_Log("Successfully got HWND! 0x%p", &hwnd);
  }

  // Enabling D3D12 debug layer
#if defined(_DEBUG)
  {
    Microsoft::WRL::ComPtr<ID3D12Debug> debugController;
    if (SUCCEEDED(D3D12GetDebugInterface(IID_PPV_ARGS(&debugController)))) {
      debugController->EnableDebugLayer();
    }
  }
#endif

  // Creating factory
  Microsoft::WRL::ComPtr<IDXGIFactory4> factory;
  ThrowIfFailed(CreateDXGIFactory1(IID_PPV_ARGS(&factory)));

  // Creating device
  if (m_useWarpDevice) {
    // TODO: put code for software renderer here - right now we work on our GPU hardware, so no code here
  } else {
    Microsoft::WRL::ComPtr<IDXGIAdapter1> hardwareAdapter;
    GetHardwareAdapter(factory.Get(), &hardwareAdapter);

    ThrowIfFailed(D3D12CreateDevice(
      hardwareAdapter.Get(),
      D3D_FEATURE_LEVEL_11_0,
      IID_PPV_ARGS(&m_device)));
  }

  // Initialization - describing and creating the command queue
  D3D12_COMMAND_QUEUE_DESC queueDesc = {};
  queueDesc.Flags                    = D3D12_COMMAND_QUEUE_FLAG_NONE;
  queueDesc.Type                     = D3D12_COMMAND_LIST_TYPE_DIRECT;

  ThrowIfFailed(m_device->CreateCommandQueue(&queueDesc, IID_PPV_ARGS(&m_commandQueue)));

  // Initialization - describing and creating the swap chain
  DXGI_SWAP_CHAIN_DESC swapChainDesc = {};
  swapChainDesc.BufferCount          = FRAME_COUNT;
  swapChainDesc.BufferDesc.Width     = m_width;
  swapChainDesc.BufferDesc.Height    = m_height;
  swapChainDesc.BufferDesc.Format    = DXGI_FORMAT_R8G8B8A8_UNORM;
  swapChainDesc.BufferUsage          = DXGI_USAGE_RENDER_TARGET_OUTPUT;
  swapChainDesc.SwapEffect           = DXGI_SWAP_EFFECT_FLIP_DISCARD;
  swapChainDesc.OutputWindow         = hwnd;
  swapChainDesc.SampleDesc.Count     = 1;
  swapChainDesc.Windowed             = TRUE;

  SDL_Log("m_swapChain  -> 0x%x", m_swapChain);
  SDL_Log("&m_swapChain -> 0x%x", &m_swapChain);

  SDL_Log("swapChainDesc  -> 0x%x", swapChainDesc);
  SDL_Log("&swapChainDesc -> 0x%x", &swapChainDesc);

  Microsoft::WRL::ComPtr<IDXGISwapChain>* swapChain;
  // FIXME: There is a bug here somewhere
  // BUG is here... is DirectX3D interferring with SDL3?
  // maybe SDL3 has internal swapchain or something like that for directx3d

  // swapChain = SDL_PROP_RENDERER_D3D12_SWAPCHAIN_POINTER;
  SDL_PropertiesID props = SDL_GetRendererProperties(renderer);
  SDL_PropertyType property_type = SDL_GetPropertyType(props, SDL_PROP_RENDERER_D3D12_SWAPCHAIN_POINTER);
  // Error in SDL_FindInHashTable for props???

  SDL_Log("Props -> 0x%x", props);
  SDL_Log("Property_type -> 0x%x", property_type);

  if (property_type == SDL_PROPERTY_TYPE_INVALID) {
    SDL_Log("Property type invalid!");
  } else {
    void* swapchainPointer = SDL_GetPointerProperty(props, SDL_PROP_RENDERER_D3D12_SWAPCHAIN_POINTER, NULL);
    if (swapchainPointer) {
      SDL_Log("swapchainPointer is 0x%p", swapchainPointer);
    } else {
      SDL_Log("Cannot find swapchainPointer!");
    }
  }
  
  /* try {
    ThrowIfFailed(factory->CreateSwapChain(
          m_commandQueue.Get(),
          &swapChainDesc,
          &swapChain
      ));
  } catch (const std::runtime_error err) {
    SDL_Log("Catched exception!");
    // SDL might have it's own swapchain...
    // Time to dig in!
  } */

  // Trying to maybe associate our swapChain to hwnd got from SDL?
  // HRESULT result;
  // result = IDXGIFactory2_CreateSwapChainForHwnd();



  // SDL_Log("m_swapChain -> %x", m_swapChain);

  /*
  ThrowIfFailed(swapChain.As(&m_swapChain));

  // Initialization - setting up fullscreen
  ThrowIfFailed(factory->MakeWindowAssociation(hwnd, DXGI_MWA_NO_ALT_ENTER));
  m_frameIndex = m_swapChain->GetCurrentBackBufferIndex();

  // Initialization - create descriptor heaps
  {
    D3D12_DESCRIPTOR_HEAP_DESC rtvHeapDesc = {};
    rtvHeapDesc.NumDescriptors             = FRAME_COUNT;
    rtvHeapDesc.Type                       = D3D12_DESCRIPTOR_HEAP_TYPE_RTV;
    rtvHeapDesc.Flags                      = D3D12_DESCRIPTOR_HEAP_FLAG_NONE;
    ThrowIfFailed(m_device->CreateDescriptorHeap(&rtvHeapDesc, IID_PPV_ARGS(&m_rtvHeap)));

    m_rtvDescriptorSize = m_device->GetDescriptorHandleIncrementSize(D3D12_DESCRIPTOR_HEAP_TYPE_RTV);
  }

  // Initialization - frame resources
  {
    CD3DX12_CPU_DESCRIPTOR_HANDLE rtvHandle(m_rtvHeap->GetCPUDescriptorHandleForHeapStart());   

    // RTV for each frame
    for (UINT n = 0; n < FRAME_COUNT; n++) {
      ThrowIfFailed(m_swapChain->GetBuffer(n, IID_PPV_ARGS(&m_renderTargets[n])));
      m_device->CreateRenderTargetView(m_renderTargets[n].Get(), nullptr, rtvHandle);
      rtvHandle.Offset(1, m_rtvDescriptorSize);
    }
  }

  ThrowIfFailed(m_device->CreateCommandAllocator(D3D12_COMMAND_LIST_TYPE_DIRECT, IID_PPV_ARGS(&m_commandAllocator)));

  // Loading assets - Hello World Triangle for now

  // Creating empy root signature
  {
    CD3DX12_ROOT_SIGNATURE_DESC rootSignatureDesc;
    rootSignatureDesc.Init(0, nullptr, 0, nullptr,
        D3D12_ROOT_SIGNATURE_FLAG_ALLOW_INPUT_ASSEMBLER_INPUT_LAYOUT);

    Microsoft::WRL::ComPtr<ID3DBlob> signature;
    Microsoft::WRL::ComPtr<ID3DBlob> error;
    ThrowIfFailed(D3D12SerializeRootSignature(&rootSignatureDesc, D3D_ROOT_SIGNATURE_VERSION_1, &signature, &error));
    ThrowIfFailed(m_device->CreateRootSignature(0,
          signature->GetBufferPointer(),
          signature->GetBufferSize(),
          IID_PPV_ARGS(&m_rootSignature)));
  }

  // Create the pipline state - includes compiling and loading shaders
  {
    Microsoft::WRL::ComPtr<ID3DBlob> vertexShader;
    Microsoft::WRL::ComPtr<ID3DBlob> pixelShader;
    Microsoft::WRL::ComPtr<ID3DBlob> vertexShaderErrorBlob;
    Microsoft::WRL::ComPtr<ID3DBlob> pixelShaderErrorBlob;
  }

#if defined(_DEBUG)
    // Enable better shader debugging with the graphics debugging tools
    UINT compileFlags = D3DCOMPILE_DEBUG | D3DCOMPILE_SKIP_OPTIMIZATION;
#else
    UINT compileFlags = 0;
#endif
    */

  return SDL_APP_CONTINUE; // This is crucial...
}

SDL_AppResult SDL_AppEvent(void* appstate, SDL_Event* event) {
  if (event->type == SDL_EVENT_QUIT) {
    return SDL_APP_SUCCESS;
  }

  // Exit on Q
  if (event->type == SDL_EVENT_KEY_DOWN) {
    // Switch on key types
    switch (event->key.key) {
      case SDLK_Q: // Exit on Q
        return SDL_APP_SUCCESS;
        break;

      default:
        break;
    }
  }

  // If everythingi is allright - proceed
  return SDL_APP_CONTINUE;
}

SDL_AppResult SDL_AppIterate(void* appstate) {
  // Runs once per frame
  return SDL_APP_CONTINUE;
}

void SDL_AppQuit(void* appstate, SDL_AppResult result) {
  // Clean stuff here - if you want of course
}
