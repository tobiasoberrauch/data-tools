from data_tools.utils import associate_screenshots_with_transcription

def test_associate_screenshots_with_single_screenshot():
    transcription = {
        'segments': [
            {'text': 'Kurz informiert bei heise online. Mit der synthetischen Stimme von Isabel Grünewald.', 'start': 3.541, 'end': 21.049},
            {'text': 'Das Portal Alle Störungen verzeichnet eine Spitze der Störungsmeldungen für Dienste wie Office 365, Minecraft oder den Microsoft Store. Die genaue Ursache der Netzprobleme ist noch unklar. Techniker von Microsoft haben jedoch bereits fehlerhafte Netzwerkpfade durch Konfigurationsänderungen überbrückt und melden eine Verbesserung der Verfügbarkeit.', 'start': 21.049, 'end': 42.961},
            {'text': 'Die Europäische Kommission plant die Entwicklung eines Alarmsystems zur Durchsetzung des Digital Services Act. Das System soll automatisiert Beweise für Verstöße sammeln und die Einhaltung des Plattformgesetzes überwachen. Für den Auftrag stehen 12 Millionen Euro zur Verfügung. Der Gewinner des 36-monatigen Vertrags soll ein Frühwarnsystem einrichten, das technologische Entwicklungen sowie neue systemische Risiken oder digitale Bedrohungen durch Plattformen in Echtzeit überwacht.', 'start': 44.053, 'end': 73.524},
            {'text': 'Apple hat die Drohung umgesetzt, neue KI-Funktionen vorerst nicht auf iPhones in Europa zu bringen. In der ersten Beta von iOS 18.1 ist Apple Intelligence zwar integriert, das Betriebssystem blockiert die Neuerungen jedoch, solange sich ein iPhone oder iPad in einem der 27 Staaten der Europäischen Union befindet.', 'start': 74.718, 'end': 95.776},
            {'text': 'Apple hatte diese Blockade im Juni in Aussicht gestellt. Grund dafür seien regulatorische Unsicherheiten durch den Digital Markets Act. Spaniens Wettbewerbsbehörde hat eine Rekordstrafe von 413,2 Millionen Euro gegen das Online-Reisebüro Booking.com ausgesprochen.', 'start': 95.776, 'end': 115.759},
            {'text': 'Grund für die Strafe ist der Vorwurf des ausbeuterischen Marktmachtmissbrauchs und des Missbrauchs der Marktmacht zum Ausschluss von Mitbewerbern. Booking.com hat angekündigt, Rechtsmittel gegen die noch nicht rechtskräftige Strafe einzulegen.', 'start': 115.759, 'end': 130.776},
            {'text': 'Der Zahlungsdienstleister PayPal konnte im zweiten Quartal des Geschäftsjahres Umsatz und Gewinn deutlich steigern. Trotz Befürchtungen, dass das Kerngeschäft unter dem verstärkten Wettbewerb von Unternehmen wie Apple oder Google leiden könnte, stieg der Umsatz um 8 Prozent auf 7,89 Milliarden US-Dollar. Der Betriebsgewinn wuchs um 17 Prozent auf 1,33 Milliarden Dollar.', 'start': 130.776, 'end': 155.23},
            {'text': 'Diese und weitere aktuelle Nachrichten finden Sie ausführlich auf heise.de', 'start': 155.23, 'end': 161.852}
        ],
        'language': 'de'
    }

    screenshots = [
        (0.04, 'screenshots/screenshot_0.png')
    ]

    expected_output = [
        ('screenshots/screenshot_0.png', 'Kurz informiert bei heise online. Mit der synthetischen Stimme von Isabel Grünewald. Das Portal Alle Störungen verzeichnet eine Spitze der Störungsmeldungen für Dienste wie Office 365, Minecraft oder den Microsoft Store. Die genaue Ursache der Netzprobleme ist noch unklar. Techniker von Microsoft haben jedoch bereits fehlerhafte Netzwerkpfade durch Konfigurationsänderungen überbrückt und melden eine Verbesserung der Verfügbarkeit. Die Europäische Kommission plant die Entwicklung eines Alarmsystems zur Durchsetzung des Digital Services Act. Das System soll automatisiert Beweise für Verstöße sammeln und die Einhaltung des Plattformgesetzes überwachen. Für den Auftrag stehen 12 Millionen Euro zur Verfügung. Der Gewinner des 36-monatigen Vertrags soll ein Frühwarnsystem einrichten, das technologische Entwicklungen sowie neue systemische Risiken oder digitale Bedrohungen durch Plattformen in Echtzeit überwacht. Apple hat die Drohung umgesetzt, neue KI-Funktionen vorerst nicht auf iPhones in Europa zu bringen. In der ersten Beta von iOS 18.1 ist Apple Intelligence zwar integriert, das Betriebssystem blockiert die Neuerungen jedoch, solange sich ein iPhone oder iPad in einem der 27 Staaten der Europäischen Union befindet. Apple hatte diese Blockade im Juni in Aussicht gestellt. Grund dafür seien regulatorische Unsicherheiten durch den Digital Markets Act. Spaniens Wettbewerbsbehörde hat eine Rekordstrafe von 413,2 Millionen Euro gegen das Online-Reisebüro Booking.com ausgesprochen. Grund für die Strafe ist der Vorwurf des ausbeuterischen Marktmachtmissbrauchs und des Missbrauchs der Marktmacht zum Ausschluss von Mitbewerbern. Booking.com hat angekündigt, Rechtsmittel gegen die noch nicht rechtskräftige Strafe einzulegen. Der Zahlungsdienstleister PayPal konnte im zweiten Quartal des Geschäftsjahres Umsatz und Gewinn deutlich steigern. Trotz Befürchtungen, dass das Kerngeschäft unter dem verstärkten Wettbewerb von Unternehmen wie Apple oder Google leiden könnte, stieg der Umsatz um 8 Prozent auf 7,89 Milliarden US-Dollar. Der Betriebsgewinn wuchs um 17 Prozent auf 1,33 Milliarden Dollar. Diese und weitere aktuelle Nachrichten finden Sie ausführlich auf heise.de')
    ]

    result = associate_screenshots_with_transcription(screenshots, transcription)
    assert result == expected_output

def test_associate_screenshots_with_transcription():
    transcription = {
        'segments': [
            {'text': 'Kurz informiert bei heise online. Mit der synthetischen Stimme von Isabel Grünewald.', 'start': 3.541, 'end': 21.049},
            {'text': 'Das Portal Alle Störungen verzeichnet eine Spitze der Störungsmeldungen für Dienste wie Office 365, Minecraft oder den Microsoft Store. Die genaue Ursache der Netzprobleme ist noch unklar. Techniker von Microsoft haben jedoch bereits fehlerhafte Netzwerkpfade durch Konfigurationsänderungen überbrückt und melden eine Verbesserung der Verfügbarkeit.', 'start': 21.049, 'end': 42.961},
            {'text': 'Die Europäische Kommission plant die Entwicklung eines Alarmsystems zur Durchsetzung des Digital Services Act. Das System soll automatisiert Beweise für Verstöße sammeln und die Einhaltung des Plattformgesetzes überwachen. Für den Auftrag stehen 12 Millionen Euro zur Verfügung. Der Gewinner des 36-monatigen Vertrags soll ein Frühwarnsystem einrichten, das technologische Entwicklungen sowie neue systemische Risiken oder digitale Bedrohungen durch Plattformen in Echtzeit überwacht.', 'start': 44.053, 'end': 73.524},
            {'text': 'Apple hat die Drohung umgesetzt, neue KI-Funktionen vorerst nicht auf iPhones in Europa zu bringen. In der ersten Beta von iOS 18.1 ist Apple Intelligence zwar integriert, das Betriebssystem blockiert die Neuerungen jedoch, solange sich ein iPhone oder iPad in einem der 27 Staaten der Europäischen Union befindet.', 'start': 74.718, 'end': 95.776},
            {'text': 'Apple hatte diese Blockade im Juni in Aussicht gestellt. Grund dafür seien regulatorische Unsicherheiten durch den Digital Markets Act. Spaniens Wettbewerbsbehörde hat eine Rekordstrafe von 413,2 Millionen Euro gegen das Online-Reisebüro Booking.com ausgesprochen.', 'start': 95.776, 'end': 115.759},
            {'text': 'Grund für die Strafe ist der Vorwurf des ausbeuterischen Marktmachtmissbrauchs und des Missbrauchs der Marktmacht zum Ausschluss von Mitbewerbern. Booking.com hat angekündigt, Rechtsmittel gegen die noch nicht rechtskräftige Strafe einzulegen.', 'start': 115.759, 'end': 130.776},
            {'text': 'Der Zahlungsdienstleister PayPal konnte im zweiten Quartal des Geschäftsjahres Umsatz und Gewinn deutlich steigern. Trotz Befürchtungen, dass das Kerngeschäft unter dem verstärkten Wettbewerb von Unternehmen wie Apple oder Google leiden könnte, stieg der Umsatz um 8 Prozent auf 7,89 Milliarden US-Dollar. Der Betriebsgewinn wuchs um 17 Prozent auf 1,33 Milliarden Dollar.', 'start': 130.776, 'end': 155.23},
            {'text': 'Diese und weitere aktuelle Nachrichten finden Sie ausführlich auf heise.de', 'start': 155.23, 'end': 161.852}
        ],
        'language': 'de'
    }

    screenshots = [
        (0.04, 'screenshots/screenshot_0.png'),
        (75.0, 'screenshots/screenshot_1.png')
    ]

    expected_output = [
        ('screenshots/screenshot_0.png', 'Kurz informiert bei heise online. Mit der synthetischen Stimme von Isabel Grünewald. Das Portal Alle Störungen verzeichnet eine Spitze der Störungsmeldungen für Dienste wie Office 365, Minecraft oder den Microsoft Store. Die genaue Ursache der Netzprobleme ist noch unklar. Techniker von Microsoft haben jedoch bereits fehlerhafte Netzwerkpfade durch Konfigurationsänderungen überbrückt und melden eine Verbesserung der Verfügbarkeit. Die Europäische Kommission plant die Entwicklung eines Alarmsystems zur Durchsetzung des Digital Services Act. Das System soll automatisiert Beweise für Verstöße sammeln und die Einhaltung des Plattformgesetzes überwachen. Für den Auftrag stehen 12 Millionen Euro zur Verfügung. Der Gewinner des 36-monatigen Vertrags soll ein Frühwarnsystem einrichten, das technologische Entwicklungen sowie neue systemische Risiken oder digitale Bedrohungen durch Plattformen in Echtzeit überwacht. Apple hat die Drohung umgesetzt, neue KI-Funktionen vorerst nicht auf iPhones in Europa zu bringen. In der ersten Beta von iOS 18.1 ist Apple Intelligence zwar integriert, das Betriebssystem blockiert die Neuerungen jedoch, solange sich ein iPhone oder iPad in einem der 27 Staaten der Europäischen Union befindet.'),
        ('screenshots/screenshot_1.png', 'Apple hatte diese Blockade im Juni in Aussicht gestellt. Grund dafür seien regulatorische Unsicherheiten durch den Digital Markets Act. Spaniens Wettbewerbsbehörde hat eine Rekordstrafe von 413,2 Millionen Euro gegen das Online-Reisebüro Booking.com ausgesprochen. Grund für die Strafe ist der Vorwurf des ausbeuterischen Marktmachtmissbrauchs und des Missbrauchs der Marktmacht zum Ausschluss von Mitbewerbern. Booking.com hat angekündigt, Rechtsmittel gegen die noch nicht rechtskräftige Strafe einzulegen. Der Zahlungsdienstleister PayPal konnte im zweiten Quartal des Geschäftsjahres Umsatz und Gewinn deutlich steigern. Trotz Befürchtungen, dass das Kerngeschäft unter dem verstärkten Wettbewerb von Unternehmen wie Apple oder Google leiden könnte, stieg der Umsatz um 8 Prozent auf 7,89 Milliarden US-Dollar. Der Betriebsgewinn wuchs um 17 Prozent auf 1,33 Milliarden Dollar. Diese und weitere aktuelle Nachrichten finden Sie ausführlich auf heise.de')
    ]

    result = associate_screenshots_with_transcription(screenshots, transcription)
    assert result == expected_output