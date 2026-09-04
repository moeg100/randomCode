#include "raylib.h"
#include <stdio.h>
#include <stdlib.h>

// =====================
// CONSTANTS
// =====================
#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 450
#define DEFAULT_TIMER 10.0f
#define TIME_INCREMENT 5.0f

#define BUTTON_WIDTH 140
#define BUTTON_HEIGHT 50
#define BUTTON_Y_POS 330
#define BUTTON_TEXT_SIZE 20

#define START_BUTTON_X 100
#define RESET_BUTTON_X 330
#define COLOR_BUTTON_X 560
#define TIME_BUTTON_X 100
#define TIME_BUTTON_Y 250

#define TITLE_X 250
#define TITLE_Y 40
#define TITLE_SIZE 30

#define TIMER_DISPLAY_X_OFFSET (SCREEN_WIDTH / 2)
#define TIMER_DISPLAY_Y 120
#define TIMER_DISPLAY_SIZE 100

#define COUNTER_DISPLAY_Y 250
#define COUNTER_DISPLAY_SIZE 30

// =====================
// BUTTON STRUCTURE
// =====================
typedef struct {
    Rectangle bounds;
    const char* label;
} Button;

// =====================
// HELPER FUNCTIONS
// =====================
Button CreateButton(float x, float y, const char* label) {
    Button btn = {
        .bounds = {x, y, BUTTON_WIDTH, BUTTON_HEIGHT},
        .label = label
    };
    return btn;
}

void DrawButton(Button btn, Color hoverColor) {
    Vector2 mouse = GetMousePosition();
    bool isHovered = CheckCollisionPointRec(mouse, btn.bounds);
    
    Color buttonColor = isHovered ? hoverColor : DARKGRAY;
    DrawRectangleRec(btn.bounds, buttonColor);
    
    // Draw border for visual feedback
    DrawRectangleLinesEx(btn.bounds, 2, isHovered ? WHITE : GRAY);
    
    // Calculate text centering
    int textWidth = MeasureText(btn.label, BUTTON_TEXT_SIZE);
    float textX = btn.bounds.x + (btn.bounds.width - textWidth) / 2;
    float textY = btn.bounds.y + (btn.bounds.height - BUTTON_TEXT_SIZE) / 2;
    
    DrawText(btn.label, (int)textX, (int)textY, BUTTON_TEXT_SIZE, WHITE);
}

int main(void)
{
    InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Raylib Timer");
    SetTargetFPS(60);

    // Timer settings
    float timer = DEFAULT_TIMER;
    float startTime = DEFAULT_TIMER;
    bool running = false;

    // Counter
    int counter = 0;

    // Timer colors for text display
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
    int backgroundIndex = 0; // Start with first color (WHITE)

    // Create buttons with labels
    Button startButton = CreateButton(START_BUTTON_X, BUTTON_Y_POS, "START");
    Button resetButton = CreateButton(RESET_BUTTON_X, BUTTON_Y_POS, "RESET");
    Button colorButton = CreateButton(COLOR_BUTTON_X, BUTTON_Y_POS, "COLOR");
    Button timeButton = CreateButton(TIME_BUTTON_X, TIME_BUTTON_Y, "+5s");

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

        // Handle button clicks
        if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
        {
            Vector2 mouse = GetMousePosition();

            // Start / Pause button
            if (CheckCollisionPointRec(mouse, startButton.bounds))
            {
                running = !running;
            }
            
            // Reset button
            if (CheckCollisionPointRec(mouse, resetButton.bounds))
            {
                timer = startTime;
                running = false;
                counter = 0;
            }

            // Change color button (cycles through timer text colors)
            if (CheckCollisionPointRec(mouse, colorButton.bounds))
            {
                colorIndex = (colorIndex + 1) % colorCount;
                // Update background color to match text color cycle
                backgroundIndex = (backgroundIndex + 1) % colorCount;
            }

            // Time button (adds time to initial setting, not running timer)
            if (CheckCollisionPointRec(mouse, timeButton.bounds))
            {
                startTime += TIME_INCREMENT;
                // Only update running timer if paused
                if (!running)
                {
                    timer = startTime;
                }
            }
        }

        // -------------------------
        // DRAW
        // -------------------------

        BeginDrawing();

        ClearBackground(timerColors[backgroundIndex]);

        // Title
        DrawText("SIMPLE RAYLIB TIMER", TITLE_X, TITLE_Y, TITLE_SIZE, RAYWHITE);

        // Timer display with minutes, seconds, and centiseconds
        int minutes = (int)timer / 60;
        int seconds = (int)timer % 60;
        int centiseconds = (int)(timer * 100) % 100;

        char timerText[32];
        snprintf(timerText, sizeof(timerText), "%02d:%02d.%02d", minutes, seconds, centiseconds);

        int textWidth = MeasureText(timerText, TIMER_DISPLAY_SIZE);

        DrawText(
            timerText,
            TIMER_DISPLAY_X_OFFSET - textWidth / 2,
            TIMER_DISPLAY_Y,
            TIMER_DISPLAY_SIZE,
            timerColors[colorIndex]
        );

        // Counter display
        char counterText[32];
        snprintf(counterText, sizeof(counterText), "Counter: %d", counter);

        DrawText(
            counterText,
            SCREEN_WIDTH / 2 - MeasureText(counterText, COUNTER_DISPLAY_SIZE) / 2,
            COUNTER_DISPLAY_Y,
            COUNTER_DISPLAY_SIZE,
            WHITE
        );

        // Draw all buttons with hover effects
        DrawButton(startButton, GRAY);
        
        // Update button label based on state
        startButton.label = running ? "PAUSE" : "START";
        
        DrawButton(resetButton, GRAY);
        DrawButton(colorButton, GRAY);
        DrawButton(timeButton, GRAY);

        EndDrawing();
    }

    CloseWindow();

    return 0;
}
