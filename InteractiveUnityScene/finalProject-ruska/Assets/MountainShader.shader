Shader "Custom/MountainTerrain"
{
    Properties
    {
        _HeightMap("Height Map", 2D) = "white" { }
        _NoiseScale("Noise Scale", float) = 1.0
        _Amplitude("Amplitude", float) = 1.0
        _Frequency("Frequency", float) = 1.0
        _CustomTime("Custom Time", float) = 0.0  
        _ObjectColor("Object Color", Color) = (1.0, 0.5, 0.5, 1.0) 
        _AmbientColor("Ambient Color", Color) = (0.1, 0.1, 0.1, 1)
        _DiffuseColor("Diffuse Color", Color) = (1, 1, 1, 1)
        _SpecularColor ("Specular Color", Color) = (1, 1, 1, 1)
        _LightPosition("Light Position", Vector) = (0, 5, 0)
        _TerrainLength("Terrain Length", float) = 10.0  
        _TerrainWidth("Terrain Width", float) = 10.0  
        _LightIntensity ("Light Intensity", Range(0, 5)) = 1.0
        _Shininess ("Shininess", Range(1, 100)) = 32
        _BumpMap("Bump Map", 2D) = "bump" { }
        _LightOn("Light On", Float) = 1.0  
    }

    SubShader
    {
        Tags { "RenderType" = "Opaque" }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float3 normal : NORMAL;
            };

            struct v2f
            {
                float4 pos : SV_POSITION;
                float3 worldPos : TEXCOORD0;
                float3 normal : TEXCOORD1;
                float2 uv : TEXCOORD2;
            };

       
            float _NoiseScale;
            float _Amplitude;
            float _Frequency;
            float _CustomTime;
            float4 _ObjectColor;
            float4 _AmbientColor;
            float4 _DiffuseColor;
            float4 _SpecularColor;
            float3 _LightPosition;
            float _TerrainLength;
            float _TerrainWidth;
            float _Shininess;
            float _LightIntensity;
            sampler2D _BumpMap;
            float _LightOn;  

            float PerlinNoise(float2 p)
            {
                return (sin(p.x * 10.0) + cos(p.y * 10.0)) * 0.5; 
            }

            float GenerateTerrainHeight(float3 position)
            {
                
                float2 noiseCoord = position.xz * _NoiseScale + _CustomTime * 0.1;
                float noiseValue = PerlinNoise(noiseCoord);
                float height = noiseValue * _Amplitude;

                return height;
            }

            v2f vert(appdata v)
            {
                v2f o;

                float xScaled = v.vertex.x * _TerrainLength;
                float zScaled = v.vertex.z * _TerrainWidth;

                float height = GenerateTerrainHeight(float3(xScaled, v.vertex.y, zScaled));
                v.vertex.y += height;

                o.pos = UnityObjectToClipPos(v.vertex);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
                o.normal = normalize(mul((float3x3)unity_ObjectToWorld, v.normal));

                o.uv = v.vertex.xz * 0.1; 

                return o;
            }

            float3 GetNormalFromBumpMap(float2 uv)
            {
                float3 bumpNormal = tex2D(_BumpMap, uv).rgb;
                bumpNormal = bumpNormal * 2.0 - 1.0;

                return normalize(bumpNormal);
            }

            // Fragment Shader Phong Lighting
            half4 frag(v2f i) : SV_Target
            {
                float3 normal = GetNormalFromBumpMap(i.uv);

                float3 lightDir = normalize(_LightPosition - i.worldPos);
                float3 reflectDir = reflect(-lightDir, normal); 
                float3 viewDir = normalize(_WorldSpaceCameraPos - i.worldPos);

                float NDotL = max(dot(normal, lightDir), 0.0);
                float4 diffuse = _DiffuseColor * NDotL;

                float RDotV = max(dot(reflectDir, viewDir), 0);
                float4 specular = _SpecularColor * pow(RDotV, _Shininess);

                float4 ambient = _AmbientColor;

                float4 outputColor = _LightIntensity * (ambient + diffuse + specular);

                outputColor *= _ObjectColor;

                if (_LightOn == 0.0)
                {
                    outputColor = ambient * _ObjectColor; 
                }

                return saturate(outputColor);
            }

            ENDCG
        }
    }

    FallBack "Diffuse"
}
