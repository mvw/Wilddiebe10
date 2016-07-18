---
title: Dokumentation zum Fachpraktikum IT­Sicherheit 2016
lang: de
author: 'Gruppe 10: Fileserver Süd'
header-includes:
    - \usepackage{fancyhdr}
    - \pagestyle{fancy}
    - \fancyhead[CO,CE]{Fileserver Süd}
    - \fancyfoot[CO,CE]{}
    - \fancyfoot[LE,RO]{\thepage}
abstract: 'Schaffen einer Kommunikationsstruktur für die Fa. Müller Backwaren.'
---
![FaPraSS16-Gruppenarbeit](images/FaPraSS16-Gruppenarbeit.jpg)
\newpage
\tableofcontents
\newpage

# Vorwort

## Zusammenfassung
Für das 'Fachpraktikum 1599 - Sicherheit im Internet' an der Fernuniversität
Hagen wurde als Aufgabenstellung folgendes Szenario gegeben:

Zwei fiktive Firmen Mayer Brot(Region Nord) und Müller Backwaren(Region Süd)
haben fusioniert. Die daraus enstehenden Anforderungen, erzeugen auch für die
EDV Abteilungen unterschiedliche Aufgaben. Um diese Aufgaben abzudecken wurden
die Studenten je Firma in 5 Gruppen eingeteilt die sich selbstständig um die
enstandenen Kernpunkte kümmern. Die Gruppeneinteilung sieht auf beiden Seiten
eine Gruppe Netzwerk, CA, Mailserver, Webserver, Fileserver. Je Gruppenpaar
gibt es eine eigenständige Aufgabe welche pro Firma und Gruppe zu erledigen
ist.

In dieser Betrachtung liegt der Fokus auf der Gruppe __Fileserver__ aus der
__Region Süd__. Diese Gruppe (Gruppe 10 - Fileserver Süd) hat die
Aufgabenstellung innerhalb des, durch die Netzwerkgruppen definierten,
Netzwerkes einen Fileserver zur Verfügung zu stellen. Hier sollen neben einem
passwordgeschützem Bereich auch ein öffentlicher Bereich zur Verfügung gestellt
werden. Die Serversysteme sollen durch die Gruppen selbst bereitgestellt
werden. Die konkrete Realisierung ist innerhalb des gegebenen Rahmes frei so
das die Wahl der eingesetzten Software wie Betriebsystem, Fileserver oder
anderweitig verwendeter Komponenten in der Aufgabe der Teilnehmer liegt.

Der Anschluss, an das durch die Netzwerkgruppen bereitgestellten Netzwerks,
wird durch die Einwahl als VPN Client auf dem jeweiligen regionalen VPN-Server
realisiert. Hierzu ist eine intensive Abstimmung mit den Gruppen Netzwerk und
CA nötig da die Kommunikation über Zertifikate mit ensprechenden
Vertrauensverhältnissen sichergestellt werden soll.

__Bearbeitungszeitraum__: Mo-18-Jul-2016 bis So-28-Aug-2016

## Teilnehmer Gruppe 10
* Silas Jansen
* Stefan Bruch
* Fabian Hofmann
* Thomas Grosswendt
* Sascha Girrulat
