#version 330
in layout(location = 0) vec3 position;
in layout(location = 1) vec2 inTexCoords;
in layout(location = 2) vec4 color;

uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

out vec2 outTexCoords;
out vec4 Col;

void main()
{
    gl_Position = projection * view * model * vec4(position, 1.0f);
    outTexCoords = inTexCoords;
    Col = color;
}