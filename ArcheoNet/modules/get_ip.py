from streamlit_js_eval import streamlit_js_eval

def pull_ip():
    ip = """
    async function getClientIP() {
        try {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        return data.ip;
        } catch (error) {
        return 'IP not available';
        }
    }
    getClientIP();
    """

    return(streamlit_js_eval(js_expressions=ip, key="pull_ip473987"))