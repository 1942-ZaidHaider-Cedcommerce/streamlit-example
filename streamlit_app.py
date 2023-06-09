import streamlit as st
import util
import os
import ai

def main():
    st.sidebar.title("My Streamlit App")
    st.sidebar.write("Navigation or additional information goes here.")

    st.title("Does this work with markup?")
    st.header("Does it?")

    prompt = util.generate_prompt()
    st.write(prompt)

    if not os.path.exists('skip_image') :
        st.write('Making Image')
        # image = ai.make_image(prompt)
        ai.upscale4x()

    st.image('image.png')
    st.image('big_image.png')

if __name__ == "__main__":
    main()
