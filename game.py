import pygame, sys
import lost_dialogue

pygame.init()

WIDTH, HEIGHT = 1100, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plato's Lost Dialogue")
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 28)

WHITE, BLACK = (255, 255, 255), (0, 0, 0)
GRAY, LIGHT_GRAY, BLUE = (
    (200, 200, 200),
    (230, 230, 230),
    (0, 120, 215),
)

input_rect = pygame.Rect(40, 40, 480, 160)
output_rect = pygame.Rect(580, 40, 480, 160)

sender_rect = pygame.Rect(40, 230, 300, 32)
receiver_rect = pygame.Rect(40, 280, 300, 32)
mood_rect = pygame.Rect(40, 330, 300, 32)

button_rect = pygame.Rect(400, 400, 120, 40)


active_box = None
texts = {
    "input": "Enter prompt.",
    "output": "",
    "sender": "Ninja",
    "receiver": "Princess",
    "mood": "Happy",
}


def process_text():
    mood = texts["mood"]
    sender = texts["sender"]
    receiver = texts["receiver"]
    prompt = texts["input"]
    return lost_dialogue.main(mood, sender, receiver, prompt)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            active_box = None
            for name, rect in [
                ("input", input_rect),
                ("sender", sender_rect),
                ("receiver", receiver_rect),
                ("mood", mood_rect),
            ]:
                if rect.collidepoint(event.pos):
                    active_box = name
            if button_rect.collidepoint(event.pos):
                texts["output"] = process_text()

        if event.type == pygame.KEYDOWN and active_box:
            if event.key == pygame.K_BACKSPACE:
                texts[active_box] = texts[active_box][:-1]
            elif event.key == pygame.K_RETURN:
                if active_box == "input":
                    texts["output"] = process_text()
            else:
                texts[active_box] += event.unicode
    screen.fill(WHITE)

    def draw_box(rect, text, label):
        pygame.draw.rect(
            screen,
            LIGHT_GRAY if active_box == label else GRAY,
            rect,
            border_radius=4,
        )
        y = rect.y + 5

        for line in text.splitlines() or [""]:
            surface = FONT.render(line, True, BLACK)
            screen.blit(surface, (rect.x + 5, y))
            y += FONT.get_height() + 2
        lbl = FONT.render(label.capitalize() + ":", True, BLACK)
        screen.blit(lbl, (rect.x, rect.y - 25))

    draw_box(input_rect, texts["input"], "input")
    draw_box(output_rect, texts["output"], "output")
    draw_box(sender_rect, texts["sender"], "sender")
    draw_box(receiver_rect, texts["receiver"], "receiver")
    draw_box(mood_rect, texts["mood"], "mood")

    pygame.draw.rect(screen, BLUE, button_rect, border_radius=6)
    btn_text = FONT.render("Submit", True, WHITE)
    screen.blit(btn_text, (button_rect.x + 25, button_rect.y + 8))

    pygame.display.flip()
    clock.tick(60)
