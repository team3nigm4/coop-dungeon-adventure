#version 330

in vec2 outTexCoords;
in float opac;
out vec4 outColor;


uniform sampler2D samplerTex;
void main()
{
    outColor = texture(samplerTex, outTexCoords) * vec4(1, 1, 1, opac);
}