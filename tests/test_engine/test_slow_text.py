from motherbrain.engine.animators.slow_text import SlowText


def test_slow_text():
    string1 = 'Hello. This is a test of the slow text animator.'
    string2 = 'Now for the glorious second line of text.' 
    st = SlowText()
    st.animate_text(string1)
    st.animate_text(string2)

