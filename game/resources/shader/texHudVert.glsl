#version 330
in layout(location = 0) vec3 position;
in layout(location = 1) vec2 inTexCoords;
in layout(location = 2) float opacity;

uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

out vec2 outTexCoords;
out float opac;

void main()
{
    gl_Position = projection * view * model * vec4(position, 1.0f);
    outTexCoords = inTexCoords;
    opac = opacity;
}