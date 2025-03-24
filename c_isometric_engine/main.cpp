#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#define SDL_MAIN_USE_CALLBACKS 1
#include <SDL3/SDL.h>
#include <SDL3/SDL_main.h>

#include <stdio.h>

#include <string>
#include <codecvt>

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

  // SDL_SysWMinfo wmInfo;
  // SDL_VERSION(*wmInfo.version);
  // if (!SDL_GetWindowWMInfo(window, &wmInfo)) {
  //   SDL_Log("Unable to get window information: %s", SDL_GetError());
  //   SDL_DestroyWindow(window);
  //   SDL_Quit();
  //   return 1;
  // }

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
