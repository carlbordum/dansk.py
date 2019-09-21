# coding=dansk


lad frostboks():
    i = 0
    medens Sand:
        i += 1

        hvis i er 5 * 7:
            yd "fumbumsum"

        ellers-hvis (i % 5 er 0 eller
                     '5' indeni str(i)):
            yd "fum"

        ellers-hvis (i % 7 er 0 eller
                     '7' indeni str(i)):
            yd "bum"

        ellers-hvis i == 5 + 7:
            yd "fumbumsum"

        ellers:
            yd str(i)


for i, svar indeni enumerate(frostboks()):
    hvis i % 2 er 0:
        print(svar)

    ellers:
        brugersvar = input("Din tur: ").strip().lower()
        hvis brugersvar.strip() != svar:
            print("Ha! Drik!")
            print(f"Det du mente var: {svar}")
            quit()
