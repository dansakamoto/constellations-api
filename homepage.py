class Homepage:
    def __init__(self, constellations):
        self.start = """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <title>Constellations API</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <meta name="description" content="An API that returns a JSON-formatted list of position data for all stars within a constellation, from the SIMBAD Astronomical Database.">
                    <link rel="preload" href="fonts/UcCo3FwrK3iLTcvsYwYZ8UA3J58.woff2" as="font" type="font/woff2" crossorigin>
                    <link rel="preload" href="fonts/UcCo3FwrK3iLTcviYwYZ8UA3.woff2" as="font" type="font/woff2" crossorigin>
                    <style>
                        /* latin-ext */
                        @font-face {
                        font-family: "Inter";
                        font-style: normal;
                        font-weight: 100 900;
                        font-display: swap;
                        src: url(fonts/UcCo3FwrK3iLTcvsYwYZ8UA3J58.woff2)
                            format("woff2");
                        unicode-range:
                            U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304,
                            U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB,
                            U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;
                        }
                        /* latin */
                        @font-face {
                        font-family: "Inter";
                        font-style: normal;
                        font-weight: 100 900;
                        font-display: swap;
                        src: url(fonts/UcCo3FwrK3iLTcviYwYZ8UA3.woff2)
                            format("woff2");
                        unicode-range:
                            U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC,
                            U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212,
                            U+2215, U+FEFF, U+FFFD;
                        }

                        :root {
                        --color1: #734b5e;
                        --color2: #f1f2ee;
                        }

                        body {
                        font-family: "Inter", sans-serif;
                        font-optical-sizing: auto;
                        font-weight: 500;
                        font-style: normal;
                        margin: 0;
                        background-color: var(--color1);
                        color: var(--color2);
                        display: flex;
                        flex-direction: column;
                        }

                        main {
                        margin: 0;
                        display: flex;
                        flex-direction: column;
                        min-height: 100vh;
                        }

                        div.header {
                        margin: 0 0 auto 0;
                        text-align: center;
                        background-color: var(--color2);
                        padding-left: 20px;
                        padding-right: 20px;
                        color: var(--color1);
                        }

                        h1 {
                        font-weight: 600;
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                        }

                        div.content {
                        text-align: center;
                        }

                        @media (width >= 40rem) {
                        div.content {
                            margin: auto 5vh;
                        }
                        }

                        @media (width >= 73rem) {
                        div.content {
                            margin: auto 20vh;
                        }
                        }

                        div.notice {
                        background-color: var(--color2);
                        color: var(--color1);
                        margin-top: auto;
                        padding-bottom: 20px;
                        padding-left: 20px;
                        padding-right: 20px;
                        text-align: center;
                        }

                        h2 {
                        font-size: medium;
                        font-weight: 900;
                        color: #222;
                        background-color: #bcbdc0;
                        padding: 5px;
                        }

                        p {
                        font-size: small;
                        letter-spacing: 0.1cap;
                        }

                        p.subtitle {
                        color: var(--color1);
                        }
                        p.subtitle a {
                        color: var(--color1);
                        }
                        p.subtitle a:hover {
                        color: var(--color1);
                        border-top: 2px solid #734b5e;
                        border-bottom: 2px solid #734b5e;
                        }

                        a {
                        color: var(--color2);
                        text-decoration: none;
                        font-weight: 600;
                        text-transform: uppercase;
                        }

                        a:hover {
                        border-top: 2px solid var(--color2);
                        border-bottom: 2px solid var(--color2);
                        }

                        a.footer-link {
                        color: var(--color1);
                        }
                        a.footer-link:hover {
                        color: var(--color1);
                        border-top: 2px solid #734b5e;
                        border-bottom: 2px solid #734b5e;
                        }

                        ul {
                        display: flex;
                        flex-wrap: wrap;
                        padding: 0;
                        }

                        li {
                        list-style-type: none;
                        margin-left: 10px;
                        font-size: large;
                        padding: 10px;
                        }

                        /*
                        animated stars by wheresdara @ codepen.io
                        https://codepen.io/wheresdara/pen/wvXBpwa
                        */
                        .stars {
                        position: fixed;
                        z-index: -1;
                        top: 50%;
                        left: 50%;
                        height: 1px;
                        width: 1px;
                        background-color: #fff;
                        border-radius: 50%;
                        box-shadow:
                            24vw 9vh 1px 0px #fff,
                            12vw -24vh 0px 1px #fff,
                            -45vw -22vh 0px 0px #fff,
                            -37vw -40vh 0px 1px #fff,
                            29vw 19vh 0px 1px #fff,
                            4vw -8vh 0px 1px #fff,
                            -5vw 21vh 1px 1px #fff,
                            -27vw 26vh 1px 1px #fff,
                            -47vw -3vh 1px 1px #fff,
                            -28vw -30vh 0px 1px #fff,
                            -43vw -27vh 0px 1px #fff,
                            4vw 22vh 1px 1px #fff,
                            36vw 23vh 0px 0px #fff,
                            -21vw 24vh 1px 1px #fff,
                            -16vw 2vh 1px 0px #fff,
                            -16vw -6vh 0px 0px #fff,
                            5vw 26vh 0px 0px #fff,
                            -34vw 41vh 0px 0px #fff,
                            1vw 42vh 1px 1px #fff,
                            11vw -13vh 1px 1px #fff,
                            48vw -8vh 1px 0px #fff,
                            22vw -15vh 0px 0px #fff,
                            45vw 49vh 0px 0px #fff,
                            43vw -27vh 1px 1px #fff,
                            20vw -2vh 0px 0px #fff,
                            8vw 22vh 0px 1px #fff,
                            39vw 48vh 1px 1px #fff,
                            -21vw -11vh 0px 1px #fff,
                            -40vw 45vh 0px 1px #fff,
                            11vw -30vh 1px 0px #fff,
                            26vw 30vh 1px 0px #fff,
                            45vw -29vh 0px 1px #fff,
                            -2vw 18vh 0px 0px #fff,
                            -29vw -45vh 1px 0px #fff,
                            -7vw -27vh 1px 1px #fff,
                            42vw 24vh 0px 0px #fff,
                            45vw -48vh 1px 0px #fff,
                            -36vw -18vh 0px 0px #fff,
                            -44vw 13vh 0px 1px #fff,
                            36vw 16vh 0px 1px #fff,
                            40vw 24vh 0px 0px #fff,
                            18vw 11vh 0px 0px #fff,
                            -15vw -23vh 1px 0px #fff,
                            -24vw 48vh 0px 1px #fff,
                            27vw -45vh 1px 0px #fff,
                            -2vw -24vh 0px 1px #fff,
                            -15vw -28vh 0px 0px #fff,
                            -43vw 13vh 1px 0px #fff,
                            7vw 27vh 1px 0px #fff,
                            47vw 5vh 0px 0px #fff,
                            -45vw 15vh 1px 1px #fff,
                            -5vw -28vh 0px 1px #fff,
                            38vw 25vh 1px 1px #fff,
                            -39vw -1vh 1px 0px #fff,
                            5vw 0vh 1px 0px #fff,
                            49vw 13vh 0px 0px #fff,
                            48vw 10vh 0px 1px #fff,
                            19vw -28vh 0px 0px #fff,
                            4vw 7vh 0px 0px #fff,
                            21vw 21vh 1px 1px #fff,
                            -15vw -15vh 0px 1px #fff,
                            -6vw -42vh 1px 0px #fff,
                            -15vw 48vh 1px 1px #fff,
                            -23vw 25vh 1px 1px #fff,
                            -48vw 25vh 0px 1px #fff,
                            -31vw -19vh 0px 1px #fff,
                            4vw 37vh 1px 1px #fff,
                            -43vw 28vh 0px 0px #fff,
                            3vw -25vh 0px 1px #fff,
                            -39vw 14vh 0px 1px #fff,
                            -40vw 31vh 0px 1px #fff,
                            35vw -36vh 1px 1px #fff,
                            16vw 49vh 0px 0px #fff,
                            6vw 39vh 0px 0px #fff,
                            3vw -35vh 0px 1px #fff,
                            -44vw -2vh 1px 0px #fff,
                            -6vw 21vh 1px 0px #fff,
                            48vw 9vh 1px 1px #fff,
                            -43vw 30vh 1px 1px #fff,
                            29vw -12vh 1px 1px #fff,
                            -48vw 13vh 1px 0px #fff,
                            -42vw 32vh 1px 1px #fff,
                            34vw 15vh 1px 1px #fff,
                            29vw -37vh 1px 1px #fff,
                            28vw 2vh 0px 0px #fff;
                        animation: zoom 100s alternate infinite;
                        }

                        @keyframes zoom {
                        0% {
                            transform: scale(1);
                        }
                        100% {
                            transform: scale(1.5);
                        }
                        }
                    </style>
                </head>
                <body>
                    <div class="stars"></div>
                    <main>
                    <div class="header">
                    <h1>Constellations API</h1>
                    <p class="subtitle">
                        An endpoint for getting JSON-formatted lists of stars by constellation region from the <a href="https://simbad.cds.unistra.fr/simbad/">SIMBAD&nbsp;Astronomical&nbsp;Database</a>.<br>Created to support artistic projects, this tool retrieves position and brightness data but may not include all of the error/precision details necessary for scientific research.
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
                        <p>Data is cached for a period of time, but constellations that haven't been viewed in a while may take a minute to load while data from SIMBAD is refreshed.</p><p><a class="footer-link" href="https://github.com/dansakamoto/constellations-api">View on github</a> for more information about what information is included in responses.</p>
                    </div>
                    </main>
                </body>
            </html>
            """

    def build(self):
        return self.start + self.links + self.end
