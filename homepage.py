class Homepage:
    def __init__(self, constellations):
        self.start = """
            <html>
                <head>
                    <title>Constellations</title>
                    <link rel="preconnect" href="https://fonts.googleapis.com">
                    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap" rel="stylesheet">
                    <link rel="stylesheet" type="text/css" href="style/main.css">
                </head>
                <body>
                    <div class="stars"></div>
                    <div class="header">
                    <h1>Constellations API</h1>
                    <p class="subtitle">Returns a JSON-formatted list of position data for all stars within a constellation - from <a href="https://simbad.cds.unistra.fr/simbad/">SIMBAD</a>
                    </div>
                    <div class="content">
                    <p>supported keys:</p>
                    <ul>
                        """

        self.links = ""
        for c in constellations:
            self.links += '<li><a href="' + c + '">' + c + "</a></li>"

        self.end = """
                    </u>
                    </div>
                    <div class="notice">
                        <p>Data is cached for a period of time, but please note that if a constellation hasn't been looked up in a while it can take several moments to get data from SIMBAD.</p>
                    </div>
                </body>
            </html>
            """

    def build(self):
        return self.start + self.links + self.end
