from pathlib import Path

content = r'''import gradio as gr
import requests
import unicodedata

BACKENDS = {
    "Local (localhost:8000)": "http://localhost:8000",
    "Production (Railway)": "https://web-production-9e1c4.up.railway.app"
}

def call_check(text, backend_choice):
    if not text.strip():
        return "कृपया मजकूर टाका."

    url = BACKENDS[backend_choice] + "/check"
    text = unicodedata.normalize("NFC", text)

    try:
        resp = requests.post(url, json={"text": text}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.ConnectionError:
        return "❌ Backend शी कनेक्शन नाही. Server चालू आहे का?"
    except Exception as e:
        return f"❌ Error: {e}"

    lines = []

    # Summary
    lines.append(
        f"**एकूण शब्द:** {data['total_words']} | "
        f"**शब्दलेखन त्रुटी:** {data['spelling_error_count']} | "
        f"**व्याकरण त्रुटी:** {data['grammar_error_count']}"
    )
    lines.append("")

    # Spelling errors
    lines.append("### 🔤 शब्दलेखन")
    if data["spelling_errors"]:
        for err in data["spelling_errors"]:
            sugg = ", ".join(err["suggestions"]) if err["suggestions"] else "—"
            lines.append(f"🔴 **{err['word']}** (स्थान: {err['char_offset']}) → सुचवण्या: {sugg}")
    else:
        lines.append("✅ शब्दलेखन बरोबर आहे.")

    lines.append("")

    # Grammar errors
    lines.append("### 📝 व्याकरण")
    if data["grammar_errors"]:
        for err in data["grammar_errors"]:
            lines.append(f"🟡 {err['message']} *(rule: {err['rule']})*")
    else:
        lines.append("✅ व्याकरण बरोबर आहे.")

    return "\n".join(lines)


def call_suggest(word, sentence, ml_ranking, backend_choice):
    if not word.strip():
        return "कृपया शब्द टाका."

    url = BACKENDS[backend_choice] + "/suggest"
    word = unicodedata.normalize("NFC", word)

    payload = {
        "word": word,
        "sentence": sentence.strip() if sentence.strip() else None,
        "ml_ranking": ml_ranking
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.ConnectionError:
        return "❌ Backend शी कनेक्शन नाही."
    except Exception as e:
        return f"❌ Error: {e}"

    suggestions = data["suggestions"]
    mode = data["ranking_mode"]

    if not suggestions:
        return f"**{word}** साठी सुचवण्या नाहीत. (mode: {mode})"

    lines = [f"**{word}** साठी सुचवण्या *(mode: {mode})*:"]
    for i, s in enumerate(suggestions, 1):
        lines.append(f"{i}. {s}")
    return "\n".join(lines)


with gr.Blocks(title="Lekhak — मराठी प्रूफरीडर") as demo:
    gr.Markdown("# 📝 Lekhak — मराठी प्रूफरीडर")
    gr.Markdown("मराठी मजकूर तपासा: शब्दलेखन, व्याकरण आणि सुधारणा सुचवण्या")

    backend_selector = gr.Radio(
        choices=list(BACKENDS.keys()),
        value="Local (localhost:8000)",
        label="Backend निवडा"
    )

    with gr.Tab("📄 मजकूर तपासा"):
        text_input = gr.Textbox(
            label="मराठी मजकूर टाका",
            placeholder="उदा. मी घरि जातो . आज  छान दिवस आहे.",
            lines=5
        )
        check_btn = gr.Button("तपासा", variant="primary")
        check_output = gr.Markdown(label="निकाल")
        check_btn.click(fn=call_check, inputs=[text_input, backend_selector], outputs=[check_output])

    with gr.Tab("💡 सुचवण्या"):
        word_input = gr.Textbox(label="चुकीचा शब्द", placeholder="उदा. घरि")
        sentence_input = gr.Textbox(
            label="संदर्भ वाक्य (ML ranking साठी, optional)",
            placeholder="उदा. मी घरि जातो"
        )
        ml_toggle = gr.Checkbox(label="MuRIL ML Ranking वापरा (local only)", value=False)
        suggest_btn = gr.Button("सुचवा", variant="primary")
        suggest_output = gr.Markdown(label="सुचवण्या")
        suggest_btn.click(
            fn=call_suggest,
            inputs=[word_input, sentence_input, ml_toggle, backend_selector],
            outputs=[suggest_output]
        )

demo.launch(server_name="0.0.0.0", server_port=7860)
'''

Path("frontend/app.py").write_text(content, encoding="utf-8")
print("frontend/app.py written — v2.0 with backend toggle + inline suggestions")