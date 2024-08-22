import pygame,sys 

def monitor_input(game):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                game.clicking[0]=True 
            elif event.button==3:
                game.clicking[1]=True 
        if event.type==pygame.MOUSEBUTTONUP:
            if event.button==1:
                game.clicking[0]=False 
            elif event.button==3:
                game.clicking[1]=False
        if event.type==pygame.KEYDOWN:
            print(f'{event.key} was pressed')
            game.key_set.add(event.key)
        if event.type==pygame.KEYUP:
            print(f'{event.key} was released')
            game.key_set.add(event.key)

        
            
