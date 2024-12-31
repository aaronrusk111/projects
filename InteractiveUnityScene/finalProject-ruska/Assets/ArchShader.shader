Shader "Custom/ArchShader"
{
    Properties
    {
        _AmbientColor ("Ambient Color", Color) = (0.1, 0.1, 0.1, 1)
        _DiffuseColor ("Diffuse Color", Color) = (1, 0.5, 0.3, 1)
        _SpecularColor ("Specular Color", Color) = (1, 1, 1, 1)
        _Shininess ("Shininess", Range(1, 100)) = 32
        _LightIntensity ("Light Intensity", Range(0, 5)) = 1.0
        _ObjectColor ("Object Color", Color) = (1, 1, 1, 1)
        _LightOn("Light On", Float) = 1.0
        _BumpMap ("Normal Map", 2D) = "bump" { }
    }

    SubShader
    {
        Tags { "RenderType"="Opaque" }
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
                float2 uv : TEXCOORD0; 
            };

            struct v2f
            {
                float4 pos : SV_POSITION;
                float3 worldPos : TEXCOORD0;
                float3 normal : TEXCOORD1;
                float2 uv : TEXCOORD2; 
            };

           
            float4 _AmbientColor;
            float4 _DiffuseColor;
            float4 _SpecularColor;
            float _Shininess;
            float _LightIntensity;
            float3 _LightPosition;
            float4 _ObjectColor;
            float _LightOn;
            sampler2D _BumpMap; 
            float4 _BumpMap_ST;

            v2f vert (appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
                o.normal = normalize(mul((float3x3)unity_ObjectToWorld, v.normal));

                o.uv = v.uv;

                return o;
            }

            
            float4 frag (v2f i) : SV_Target
            {
                float3 lightDir = normalize(_LightPosition - i.worldPos);
                float3 normal = normalize(i.normal);

            
                float3 normalMap = tex2D(_BumpMap, i.uv).rgb;
                normalMap = normalMap * 2.0 - 1.0;  
                normal = normalize(normal + normalMap);

    
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
}
