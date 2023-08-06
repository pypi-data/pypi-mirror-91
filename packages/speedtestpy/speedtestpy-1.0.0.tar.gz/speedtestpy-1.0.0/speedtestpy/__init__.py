import speedtest

st = speedtest.Speedtest()


class data:
    def download(self=None):
        print(st.download())

    def upload(self=None):
        print(st.upload())

    def ping(self=None):
        servernames = []
        st.get_servers(servernames)
        print(st.results.ping)


class run:
    def help(self=None):
        print("""run.test() runs full speedtest.
run.simple() prints in this order:
        
- download
- upload
- ping""")

    def simple(self=None):
        data.download()
        data.upload()
        data.ping()

    def test(self=None):
        speedtest.main()
