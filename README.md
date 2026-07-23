# Projects

Custom Ray tracer: it's a lightweight, multi-threaded C++17 CPU path(ray)tracer built completely from scratch in a single headerless source file. It renders realistic raytraced scenes with global illumination, reflections, refractions, and anti-aliasing directly to an output .ppm image. I made it mostly to fiddle around with my understanding of light.
  Materials: Matte, Metal, Dielectric (glass for refraction). 
Note that game engines cannot run this code!!! it doesnt have DirectX, Raytracing/DXR, Vulkan KHR blablabla... But if you do want to make a custom raytracer in a game engine, you are welcome to extrapolate the applied math and physics ;)

Febbrario 2026 Hackaton backend: un backend per un centro gestionale di pannelli solari, realizzato in 3 giorni con Python, estrapola informazioni da un API di meteo per calcolare vari output, mandandoli a un certo url utilizzando Flask. Per integrarlo con il sito html e js (fatto dai miei 2 colleghi), ho utilizzato Jinja2. 
