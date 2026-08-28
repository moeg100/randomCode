#include <SDL2/SDL.h>
#include <stdio.h>
#include <SDL2/SDL_main.h>

#include <stdbool.h>
#define HEIGHT 720
#define WEIGHT 1080



int main(){

SDL_Window * win =  SDL_CreateWindow("TEst", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, WEIGHT, HEIGHT, SDL_WINDOW_SHOWN);


SDL_Renderer * rend  = NULL;
rend = SDL_CreateRenderer(win, 1, SDL_RENDERER_SOFTWARE);

SDL_SetRenderDrawColor(rend, 87, 58, 64, 255/2);

SDL_RenderClear(rend);


SDL_Rect squareLike;

squareLike.x = 50;
squareLike.y = 50;
squareLike.w = 500;
squareLike.h = 500;

SDL_SetRenderDrawColor(rend, 212, 21, 91, 255);
SDL_RenderFillRect(rend, &squareLike);


SDL_RenderPresent(rend);

//SDL_Delay(5000);


bool quit = false;
SDL_Event e;
int i = 0;
int j = 0;

bool check = true;
while(!quit){
	while(SDL_PollEvent(&e)){

		if(e.type == SDL_QUIT){
		quit = true;
}
}

if(i < WEIGHT && check){
      SDL_SetRenderDrawColor(rend, 252, 186, 3, 255);

      SDL_RenderDrawPoint(rend, i, j);
      i++;
      
      SDL_RenderPresent(rend);
      SDL_Delay(5);

    }
  else{
       SDL_SetRenderDrawColor(rend, 212, 21, 91, 255);

    if(check){
      check = false;
      j++;
      }
      //j++;
 SDL_RenderDrawPoint(rend, i, j);
      --i;

      if(i == 0){
        //i = 1;
        SDL_RenderDrawPoint(rend, i, j);

        j++;
        check = true;

      }

//      SDL_RenderDrawPoint(rend, i, j);
      SDL_RenderPresent(rend);
      SDL_Delay(5);
    }
    
}


SDL_DestroyWindow(win);
SDL_Quit();


	return EXIT_SUCCESS;



}
