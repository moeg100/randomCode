#include "raylib.h"
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    const int screenWidth = 800;
    const int screenHeight = 450;

    InitWindow(screenWidth, screenHeight, "Raylib Timer");
    SetTargetFPS(60);

    // Timer settings
    float timer = 10.0f;
    float startTime = 10.0f;
    bool running = false;

    // Counter
    int counter = 0;

    // Timer colors
    Color timerColors[] = {
        WHITE,
        SKYBLUE,
        GREEN,
        YELLOW,
        ORANGE,
        RED,
        PINK,
        PURPLE,
        BLACK
    };

    int colorIndex = 0;
    int colorCount = sizeof(timerColors) / sizeof(timerColors[0]);
    int backgroundIndex = GetRandomValue(0, colorCount - 1); // or rand() % colorCount

    // Buttons
    Rectangle startButton = { 100, 330, 140, 50 };
    Rectangle resetButton = { 330, 330, 140, 50 };
    Rectangle colorButton = { 560, 330, 140, 50 };
    Rectangle timeButton =  {100, 250, 140, 50 };

    while (!WindowShouldClose())
    {
        // -------------------------
        // UPDATE
        // -------------------------

        if (running)
        {
            timer -= GetFrameTime();

            if (timer <= 0.0f)
            {
                timer = startTime;
                counter++;
            }
        }

        // Start / Pause button
        if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
        {
            Vector2 mouse = GetMousePosition();

            if (CheckCollisionPointRec(mouse, startButton))
            {
                running = !running;
            }
            // Reset button
            if (CheckCollisionPointRec(mouse, resetButton))
            {
                timer = startTime;
                running = false;
                counter = 0;
            }

            // Change color button
            if (CheckCollisionPointRec(mouse, colorButton))
            {
                colorIndex++;

                if (colorIndex >= colorCount)
                {
                    colorIndex = 0;
                }
                backgroundIndex = GetRandomValue(0, colorCount - 1); // update background only now

            }

            if (CheckCollisionPointRec(mouse, timeButton)){
              timer += 5.0f;
              startTime = timer;
          }
        }

        // -------------------------
        // DRAW
        // -------------------------

        BeginDrawing();

        ClearBackground(timerColors[backgroundIndex]);

        // Title
        DrawText("SIMPLE RAYLIB TIMER", 250, 40, 30, RAYWHITE);

        // Timer
        int seconds = (int)timer;

        char timerText[32];
        sprintf(timerText, "%02d", seconds);

        int textWidth = MeasureText(timerText, 100);

        DrawText(
            timerText,
            screenWidth / 2 - textWidth / 2,
            120,
            100,
            timerColors[colorIndex]
        );

        // Counter
        char counterText[32];
        sprintf(counterText, "Counter: %d", counter);

        DrawText(
            counterText,
            screenWidth / 2 - MeasureText(counterText, 30) / 2,
            250,
            30,
            WHITE
        );

        // Start / Pause button
        DrawRectangleRec(startButton, DARKGRAY);

        if (running)
            DrawText("PAUSE", 135, 345, 20, WHITE);
        else
            DrawText("START", 135, 345, 20, WHITE);

        // Reset button
        DrawRectangleRec(resetButton, DARKGRAY);
        DrawText("RESET", 365, 345, 20, WHITE);

        // Color button
        DrawRectangleRec(colorButton, DARKGRAY);
        DrawText("COLOR", 595, 345, 20, WHITE);

        DrawRectangleRec(timeButton, DARKGRAY);
        DrawText("TIME", 140, 260, 20, WHITE);

        EndDrawing();
    }

    CloseWindow();

    return 0;
}
