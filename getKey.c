#include <stdio.h>
#include <stdlib.h>
#include <openssl/evp.h>
#include <string.h>


const char *PLAIN_DATA = "This is a top secret.";

unsigned char custom_iv[16] = {
    0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x00, 0x99,
    0x88, 0x77, 0x66, 0x55, 0x44, 0x33, 0x22, 0x11
};

unsigned char target_cipher_text[32] = {
    0x76, 0x4A, 0xA2, 0x6B, 0x55, 0xA4, 0xDA, 0x65,
    0x4D, 0xF6, 0xB1, 0x9E, 0x4B, 0xCE, 0x00, 0xF4,
    0xED, 0x05, 0xE0, 0x93, 0x46, 0xFB, 0x0E, 0x76,
    0x25, 0x83, 0xCB, 0x7D, 0xA2, 0xAC, 0x93, 0xA2
};

size_t target_len = 32;

int main(){

//printf("%s", PLAIN_DATA);

    FILE *file = fopen("words.txt", "r");
    if (!file) {
        perror("Error opening words.txt");
        return 1;
    }

    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();

    char word[256];
    int key_found = 0;


  while (fscanf(file, "%255s", word) == 1) {
        size_t word_len = strlen(word);

        if (word_len <= 16) {
            size_t padding_len = 16 - word_len;
            if (padding_len == 0) {
                padding_len = 16;
            }

        unsigned char guess_key[16];
        memcpy(guess_key, word, word_len);
        memset(word_len + guess_key, 0x23, padding_len);


        unsigned char out_buf[64];
        int out_len1 = 0, out_len2 = 0;


        if (EVP_EncryptInit_ex(ctx, EVP_aes_128_cbc(), NULL, guess_key, custom_iv) != 1) continue;
        if (EVP_EncryptUpdate(ctx, out_buf, &out_len1, (unsigned char*)PLAIN_DATA, strlen(PLAIN_DATA)) != 1) continue;
        if (EVP_EncryptFinal_ex(ctx, out_buf + out_len1, &out_len2) != 1) continue;


        int total_cipher_len = out_len1 + out_len2;

        if (total_cipher_len == (int)target_len && memcmp(out_buf, target_cipher_text, target_len) == 0) {
                printf("Found the Key ");
                for (int i = 0; i < 16; i++) {
                    printf("%02x", guess_key[i]);
                }
                printf(", with the word %s\n", word);
                key_found = 1;
                break;
            }

     }

}

  if (!key_found) {
        printf("key was not found\n");
    }


    EVP_CIPHER_CTX_free(ctx);
    fclose(file);

  return 0;
}
