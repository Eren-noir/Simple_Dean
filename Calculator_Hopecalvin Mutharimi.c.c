/*
 * Simple Calculator Program
 * Description: A menu-driven calculator with basic arithmetic operations,
 *              advanced functions (power, square root, percentage),
 *              and memory storage capabilities.
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>  // For pow() and sqrt() functions

// Global variables for calculator state
float memory = 0.0;      // Memory storage for calculator
float last_result = 0.0; // Stores the last calculated result
int has_result = 0;      // Flag to track if a result exists

/**
 * Displays the main calculator menu and gets user choice
 * Returns: integer representing user's menu choice (1-10)
 */
int menu() {
    int choice;
    printf("Menu:\n");
    printf("1. Addition\n");
    printf("2. Subtraction\n");
    printf("3. Multiplication\n");
    printf("4. Division\n");
    printf("5. Power (x^y)\n");
    printf("6. Square root\n");
    printf("7. Percentage\n");
    printf("8. Memory Recall (MR)\n");
    printf("9. Memory Clear (MC)\n");
    printf("10. Exit\n");
    printf("Enter choice:\n");
    scanf("%d", &choice);
    return choice;
}

/**
 * Performs the selected mathematical operation
 * Parameters:
 *   a - first operand
 *   b - second operand (not used for square root)
 *   choice - operation type (1-7)
 * Returns: result of the mathematical operation
 */
float operation(float a, float b, int choice) {
    switch (choice) {
    case (1):  // Addition
        return a + b;
        break;
    case (2):  // Subtraction
        return a - b;
        break;
    case (3):  // Multiplication
        return a * b;
        break;
    case (4):  // Division with zero-division protection
        while (b == 0) {
            printf("Sorry, division by zero is not allowed!\n");
            printf("Please input the second number again:\n");
            scanf("%f", &b);
        }
        return a / b;
        break;
    case (5):  // Power calculation (a^b)
        return pow(a, b);
        break;
    case (6):  // Square root (only uses first number)
        if (a < 0) {
            printf("Cannot calculate square root of negative number!\n");
            return 0;
        }
        return sqrt(a);
        break;
    case (7):  // Percentage calculation (a% of b = a*b/100)
        return (a * b) / 100;
        break;
    default:
        printf("Invalid! Please enter a valid choice\n");
        return 0;
    }
}

/**
 * Gets a number from user input or recalls from memory
 * Parameters:
 *   prompt - string to display to user
 * Returns: float value entered by user or memory value
 */
float get_number(const char* prompt) {
    char input[20];  // Buffer for user input
    printf("%s", prompt);
    scanf("%s", input);

    // Check if user wants to recall from memory
    if (input[0] == 'M' || input[0] == 'm') {
        printf("Using memory value: %.2f\n", memory);
        return memory;
    } else {
        // Convert string to float
        return atof(input);
    }
}

/**
 * Main program loop - handles menu selection and operation execution
 */
int main() {
    char continue_choice;

    // Main program loop
    do {
        int choice = menu();

        // Handle exit option
        if (choice == 10) {
            printf("Thanks for taking a look\n");
        }
        // Handle memory recall
        else if (choice == 8) {
            printf("Memory contains: %.2f\n", memory);
        }
        // Handle memory clear
        else if (choice == 9) {
            memory = 0;
            printf("Memory cleared.\n");
        }
        // Handle operations requiring two numbers
        else if (choice >= 1 && choice <= 5 || choice == 7) {
            float a, b;

            // Get first number
            a = get_number("Please enter the first number (or 'M' for memory): \n");

            // Special handling for percentage display
            if (choice == 7) {
                b = get_number("Please enter the second number (percentage of what): \n");
                printf("%.2f%% of %.2f = ", a, b);
            } else {
                b = get_number("Please enter the second number (or 'M' for memory): \n");
            }

            // Perform calculation
            float result = operation(a, b, choice);
            printf("Result: %.2f\n", result);

            // Store result for potential future use
            last_result = result;
            has_result = 1;

            // Ask user if they want to save result to memory
            char save_choice;
            printf("Do you want to save this result to memory? (y/n): ");
            scanf(" %c", &save_choice);

            if (save_choice == 'y' || save_choice == 'Y') {
                memory = result;
                printf("Result %.2f added to memory. Memory now contains: %.2f\n", result, memory);
            }
        }
        // Handle square root (single number operation)
        else if (choice == 6) {
            float a;

            // Get number for square root calculation
            a = get_number("Please enter the number (or 'M' for memory): \n");

            // Calculate square root (b parameter not used)
            float result = operation(a, 0, choice);
            printf("Result: %.2f\n", result);

            // Store result
            last_result = result;
            has_result = 1;

            // Ask user if they want to save result to memory
            char save_choice;
            printf("Do you want to save this result to memory? (y/n): ");
            scanf(" %c", &save_choice);

            if (save_choice == 'y' || save_choice == 'Y') {
                memory = result;
                printf("Result %.2f added to memory. Memory now contains: %.2f\n", result, memory);
            }
        }
        // Handle invalid menu choices
        else {
            printf("Invalid choice! Please try again.\n");
        }

    }
    while (continue_choice == 'y');

    // Exit message
    if (continue_choice == 'n') {
        printf("Sad to see you leave.\n");
    }

    return 0;
}
