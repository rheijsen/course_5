import os
from sys import argv


def mafft(msa_file, msa_output):
    """ Deze functie voert een MSA uit via MAFFT via een command in de terminal

    :param msa_file: Fasta bestand met de sequenties die je wilt alignen
    :param msa_output: Bestand waar de alignment naar toe moet worden geschreven
    """
    if os.path.isfile(msa_output):
        # Foutmelding voor wanneer bestand bestand met MSA al bestaat
        print("Bestand voor MSA bestaat al! Kies een andere naam.")
        exit()
    else:
        os.system('mafft "{}" > "{}"'.format(msa_file, msa_output))
        print("MSA succesvol uitgevoerd!")
    return


def hmmbuild(msa_output, hmm_output):
    """ Deze functie maak een HMM profiel van de MSA via de een command in de terminal

    :param msa_output: Bestand met daarin de alignment waarvan je een HMM profiel wilt maken
    :param hmm_output: Bestand waar het HMM profiel naar toe moet worden geschreven
    """
    if os.path.isfile(hmm_output):
        # Foutmelding voor wanneer bestand met HMM output al bestaat
        print("Bestand voor HMM bestaat al! Kies een andere naam.")
        exit()
    elif not os.path.isfile(msa_output):
        # Foutmelding voor wanneer MSA bestand niet kan worden gevonden
        print("Bestand met MSA kan niet worden gevonden! Er kan geen HMM profiel worden gemaakt!")
        exit()
    else:
        os.system('hmmbuild "{}" "{}"'.format(hmm_output, msa_output))
        print("HHMbuild succesvol uitgevoerd!")
    return


def hmmsearch(hmmsearch_input, hmmsearch_output, database):
    """ Deze functie zoek aan de hand van een HMM profiel in een database

    :param hmmsearch_input: Bestand met daarin het HMM profiel waarmee je tegen de database wilt zoeken
    :param hmmsearch_output: Bestand waar het de resultaten van de HMM search naar toe moeten worden geschreven
    :param database: Database waarin moet worden gezocht
    :return:
    """
    if os.path.isfile(hmmsearch_output):
        # Foutmelding voor wanneer bestand met HMMsearch output al bestaat
        print("Bestand voor HMMsearch output bestaat al! Kies een andere naam")
        exit()
    elif not os.path.isfile(hmmsearch_input):
        # Foutmelding voor wanneer bestand met HMM profiel niet kan worden gevonden
        print("Bestand met HMM profiel kan niet worden gevonden! HMMsearch kan niet worden uitgevoerd!")
        exit()
    else:
        os.system('hmmsearch --noali -A "{}" "{}" "{}"'.format(hmmsearch_output, hmmsearch_input, database))
        print("HMMsearch succesvol uitgevoerd!")
    return


def stockholm_to_fasta(fasta_output, hmmsearch_input):
    """ Deze functie converteert een stockholm format naar een fasta format

    :param fasta_output: Bestand waar de output naar toe moet worden geschreven
    :param hmmsearch_input: Bestand dat moet om worden gezet naar Fasta format
    """
    if os.path.isfile(fasta_output):
        # Foutmelding voor wanneer bestand met fasta output al bestaat
        print("Fasta bestand bestaat al! Kies een andere naam.")
        exit()
    elif not os.path.isfile(hmmsearch_input):
        # Foutmelding voor wanneer HMMserach bestand niet kan worden gevonden
        print("HMMsearch bestand kan niet worden gevonden! Bestand kan niet worden omgezet naar fasta!")
        exit()
    else:
        os.system('./esl-reformat -o "{}" -u fasta "{}"'.format(fasta_output, hmmsearch_input))
        print("Stockholm format succesvol omgezet naar Fasta")
    return


def jalview(msa_output):
    """ Deze functie geeft het eindresultaat weer in Jalview

    :param msa_output: Bestand met daarin de MSA
    """
    if not os.path.isfile(msa_output):
        print("MSA bestand kan niet worden gevonden! MSA kan niet worden weergegeven in Jalview")
    else:
        os.system('/home/rik/opt/jalview/jalview --args -open "{}"'.format(msa_output))
    return


if __name__ == '__main__':
    try:
        # Fasta bestand waarvan je de MSA wilt maken
        fasta_input = argv[1]
        # Naam voor MSA output bestand
        msa_output = argv[2]
        # Naam voor HMMsearch output
        hmmsearch_output = argv[3]
        # Naam voor fasta na HMMsearch
        hmmsearch_fasta_output = argv[4]
        # Aantal iteraties
        aantal_iteraties = int(argv[5])
        # Locatie database
        database = argv[6]
        # Resultaten bekijken in jalview ja of nee
        jalview_resultaat = argv[7]

        # Folder waarin de resultaten worden opgeslagen
        resultaten_folder = "./resultaten/"
        nieuwe_fasta = ""
        msa_output_per_iteratie = ""
        for i in range(aantal_iteraties):
            # De locatie waar de resultaten van MAFFT moeten worden opgeslagen
            msa_output_per_iteratie = resultaten_folder + msa_output + str(i + 1) + ".fasta"
            # Bij de eerste iteratie moet het Fasta bestand worden gebruikt die meegegeven is
            if i == 0:
                mafft(fasta_input, msa_output_per_iteratie)
            else:
                mafft(nieuwe_fasta, msa_output_per_iteratie)

            # Locatie waar de HMMbuild resultaten moeten worden opgeslagen
            hmmbuild_output_per_iteratie = resultaten_folder + msa_output + str(i + 1) + ".hmm"
            hmmbuild(msa_output_per_iteratie, hmmbuild_output_per_iteratie)

            # Locatie waar de HMMsearch resultaten moeten worden opgeslagen
            hmmsearch_output_per_iteratie = resultaten_folder + hmmsearch_output + str(i + 1) + ".hmmsearch"
            hmmsearch(hmmbuild_output_per_iteratie, hmmsearch_output_per_iteratie, database)

            # Locatie waar de Fasta format van HMMsearch moet worden opgeslagen
            hmmsearch_to_fasta_output_per_iteratie = resultaten_folder + hmmsearch_fasta_output + str(i + 1) + ".fasta"
            nieuwe_fasta = hmmsearch_to_fasta_output_per_iteratie
            stockholm_to_fasta(hmmsearch_to_fasta_output_per_iteratie, hmmsearch_output_per_iteratie)
        mafft(nieuwe_fasta, msa_output_per_iteratie)
        nieuwe_fasta = resultaten_folder + msa_output + str(aantal_iteraties) + ".fasta"
        if jalview_resultaat == "ja":
            jalview(nieuwe_fasta)
    except IndexError:
        print("Onjuist gebruik van de pipeline. Gebruik de volgende layout."
              "\npython3 pipeline.py [Fasta input] [MSA output] [HMMsearch output] [Fasta output] [Aantal iteraties] "
              "[locatie database] [resultaten bekijken in jalview: ja of nee]")
    except ValueError:
        print("Vul een getal in bij het aantal iteraties")
