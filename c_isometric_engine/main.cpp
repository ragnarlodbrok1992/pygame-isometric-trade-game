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
// static float m_aspectRatio = static_cast<float>(m_width) / static_cast<float>(m_height);
static std::wstring title = L"SDL Isometric Trade Game";
static std::wstring version = L"alpha";
static std::wstring identifier = L"ragnar.engine.ISOMETRIC";
static std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;

// Helper function to enumerate properties in SDL
static void enumerate_properties(void* userdata, SDL_PropertiesID props, const char* name) {
  SDL_PropertyType prop_type = SDL_GetPropertyType(props, name);

  switch (prop_type) {
    case SDL_PROPERTY_TYPE_POINTER:
      SDL_Log("%s is a pointer poperty", name);
      break;
    case SDL_PROPERTY_TYPE_STRING:
      SDL_Log(
        "%s is a string property with value %s", name, SDL_GetStringProperty(props, name, ""));
      break;
    case SDL_PROPERTY_TYPE_NUMBER:
      SDL_Log("%s is a number property with value %" SDL_PRIs64, name, SDL_GetNumberProperty(props, name, 0));
      break;
    case SDL_PROPERTY_TYPE_FLOAT:
      SDL_Log("%s is a float property with value %f", name, SDL_GetFloatProperty(props, name, 0.0f));
      break;
    case SDL_PROPERTY_TYPE_BOOLEAN:
      SDL_Log(
        "%s is a boolean property with value %d", name, SDL_GetBooleanProperty(props, name, false));
      break;
    case SDL_PROPERTY_TYPE_INVALID:
    default:
      SDL_Log("%s is an invalid property", name);
      break;
  }
}

SDL_AppResult SDL_AppInit(void** appstate, int argc, char* argv[]) {
  SDL_SetAppMetadata(converter.to_bytes(title).c_str(),
      converter.to_bytes(version).c_str(),
      converter.to_bytes(identifier).c_str());

  if (!SDL_Init(SDL_INIT_VIDEO)) {
    SDL_Log("Couldn't initialize SDL: %s", SDL_GetError());
    return SDL_APP_FAILURE;
  }

  SDL_SetHint(SDL_HINT_RENDER_DRIVER, "direct3d12");
  if (!SDL_CreateWindowAndRenderer("SDL Isometric Trade Game",
        m_width, m_height,
        0, &window, &renderer)) {
    SDL_Log("Couldn't create window/renderer: %s", SDL_GetError());
    return SDL_APP_FAILURE;
  }

  SDL_PropertiesID renderer_properties_id = SDL_GetRendererProperties(renderer);

  int num_displays;
  SDL_DisplayID* displays = SDL_GetDisplays(&num_displays);
  SDL_Log("Found %d displays.", num_displays);

  for (int i = 0; i < num_displays; i++) {
    SDL_PropertiesID prop_id = SDL_GetDisplayProperties(displays[i]);
    SDL_Log("Display %d has properties ID %d", i, prop_id);

    if (!SDL_EnumerateProperties(prop_id, enumerate_properties, NULL)) {
      SDL_Log("Error enumerating display properties: %s.", SDL_GetError());
    }
  }

  if (!SDL_EnumerateProperties(renderer_properties_id, enumerate_properties, NULL)) {
    SDL_Log("Error enumerating renderer properties: %s.", SDL_GetError());
  }

  // Let's try to use directx3d12 devices/command_queue/swap_chain provided to us by SDL3...

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
