
import pygame
pygame.init()
while True:
    for event in pygame.event.get():
        print("got it")
        if event.type == KEYDOWN:
            key_input = pygame.key.get_pressed()

            # complex orders
            if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                print("Forward Right")

            elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                print("Forward Left")

            elif key_input[pygame.K_0]:
                print("Forward")

            elif key_input[pygame.K_DOWN]:
                print("Reverse")

            elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                print('exit')
                keep_running = False
                break
                    
        elif event.type == pygame.KEYUP:
            print("up")
            break