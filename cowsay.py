import sys
import os
import textwrap
import argparse

def get_cow(cow_name, cow_path):
    # .cow uzantısını kontrol et
    if not cow_name.endswith('.cow'):
        cow_name += '.cow'
    
    # Cow dosyasını bul
    full_path = os.path.join(cow_path, cow_name)
    if not os.path.exists(full_path):
        return f"Hata: {cow_name} bulunamadı!"

    with open(full_path, 'r') as f:
        content = f.read()
    
    # Perl değişkenlerini Python formatına basitçe uyarla
    # Bu kısım paylaştığın get_cow mantığının basitleştirilmiş halidir [cite: 66]
    return content

def construct_balloon(message, width=40):
    lines = textwrap.wrap(message, width=width)
    max_len = max(len(line) for line in lines)
    
    output = " " + "_" * (max_len + 2) + "\n"
    if len(lines) == 1:
        output += f"< {lines[0]} >\n"
    else:
        output += f"/ {lines[0].ljust(max_len)} \\\n"
        for line in lines[1:-1]:
            output += f"| {line.ljust(max_len)} |\n"
        output += f"\\ {lines[-1].ljust(max_len)} /\n"
    
    output += " " + "-" * (max_len + 2)
    return output

def main():
    # Paylaştığın cowsay.1 manuelindeki argümanlar [cite: 4, 10, 11, 12]
    parser = argparse.ArgumentParser()
    parser.add_argument('message', nargs='*', default=[])
    parser.add_argument('-f', '--file', default='default.cow')
    parser.add_argument('-e', '--eyes', default='oo')
    parser.add_argument('-T', '--tongue', default='  ')
    parser.add_argument('-W', '--width', type=int, default=40)
    
    # Modlar (Borg, Dead, vb.) [cite: 36, 55-61]
    parser.add_argument('-b', action='store_true') # Borg
    parser.add_argument('-d', action='store_true') # Dead
    parser.add_argument('-g', action='store_true') # Greedy
    parser.add_argument('-p', action='store_true') # Paranoid
    parser.add_argument('-s', action='store_true') # Stoned
    
    args = parser.parse_args()
    
    # Göz ve Dil mantığı [cite: 55-61]
    eyes = args.eyes[:2]
    tongue = args.tongue[:2]
    if args.b: eyes = "=="
    if args.d: eyes = "xx"; tongue = "U "
    if args.g: eyes = "$$"
    if args.p: eyes = "@@"
    if args.s: eyes = "**"; tongue = "U "

    # Mesajı birleştir
    message = " ".join(args.message) if args.message else sys.stdin.read().strip()
    
    if not message:
        return

    # Klasör yapısına göre cowpath ayarla 
    cow_path = os.path.join(os.path.dirname(__file__), 'cows')
    
    balloon = construct_balloon(message, args.width)
    cow_template = get_cow(args.file, cow_path)
    
    # Cow dosyasındaki Perl değişkenlerini yerleştir
    cow = cow_template.replace('$eyes', eyes).replace('$tongue', tongue).replace('$thoughts', '\\')
    # Perl'in EOC/heredoc kısımlarını temizle
    cow = cow.split('EOC')[1] if 'EOC' in cow else cow

    print(balloon)
    print(cow)

if __name__ == "__main__":
    main()