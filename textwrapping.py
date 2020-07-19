def blit_text(surface, text, pos, font, color, secondary_color, interline, max_width, words_to_color):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    lines = 0

    x, y = pos
    for line in words:
        for i, word in enumerate(line):
            if i < words_to_color:
                word_surface = font.render(word, True, secondary_color)
            else:
                word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height * interline # Start on new row.
                lines += 1
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

    return lines