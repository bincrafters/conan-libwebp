#include <stdio.h>
#include <webp/decode.h>
#include <webp/encode.h>

int main()
{
    int version = WebPGetDecoderVersion();
    printf("decoder v%d.%d.%d\n", version >> 16, (version >> 8) & 0xF, version & 0xF);
    version = WebPGetEncoderVersion();
    printf("encoder v%d.%d.%d\n", version >> 16, (version >> 8) & 0xF, version & 0xF);
    return 0;
}