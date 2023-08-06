import curses
import click


@click.command()
@click.argument("input_file", type=click.File(mode="r"), required=True)
@click.option("-s", "--speed", type=click.IntRange(min=1), 
              default=1, help="Typing speed (characters per keypress)")
@click.option("--skip", "skip_lines", type=click.IntRange(min=0), 
              default=0, help="Skip first N lines")
@click.option("--loop/--no-loop", is_flag=True, default=True, 
              help="Loop over the input file infinitely")
def cli(input_file, speed, skip_lines, loop):
    lines = input_file.readlines()
    skipped_lines, lines = lines[:skip_lines], lines[skip_lines:]
    if len(lines) == 0:
        click.echo("error: can't skip more lines than the file contains", err=True)
        return

    skipped_text = ''.join(skipped_lines)
    text = ''.join(lines)

    def main(win):
        ptr = 0

        win.nodelay(True)
        win.scrollok(True)
        win.clear()                
        win.addstr(skipped_text)
        while True:          
            try:                 
                win.getkey()         
                chunk = text[ptr:ptr+speed]
                win.addstr(chunk)
                ptr += speed
                if loop:
                    ptr %= len(text)
                elif ptr >= len(text):
                    break
            except KeyboardInterrupt:
                break
            except:
                pass         
        return True

    curses.wrapper(main)

if __name__ == "__main__":
    cli()