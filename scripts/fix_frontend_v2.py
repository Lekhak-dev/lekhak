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

    total_words = data.get("total_words", "?")
    spell_count = data.get("spelling_error_count", "?")
    grammar_count = data.get("grammar_error_count", "?")
    spelling_errors = data.get("spelling_errors", [])
    grammar_errors = data.get("grammar_errors", [])

    sections = []

    # Summary box
    sections.append(
        f"> **एकूण शब्द:** {total_words} &nbsp;|&nbsp; "
        f"**शब्दलेखन त्रुटी:** {spell_count} &nbsp;|&nbsp; "
        f"**व्याकरण त्रुटी:** {grammar_count}"
    )

    # Spelling section
    sections.append("### 🔤 शब्दलेखन")
    if spelling_errors:
        spell_lines = []
        for err in spelling_errors:
            word = err.get("word", "?")
            offset = err.get("char_offset", "?")
            suggestions = err.get("suggestions", [])
            sugg = " / ".join(suggestions) if suggestions else "—"
            spell_lines.append(f"🔴 **{word}** &nbsp;→&nbsp; {sugg} &nbsp;*(स्थान: {offset})*")
        sections.append("\n\n".join(spell_lines))
    else:
        sections.append("✅ शब्दलेखन बरोबर आहे.")

    # Grammar section
    sections.append("### 📝 व्याकरण")
    if grammar_errors:
        grammar_lines = []
        for err in grammar_errors:
            message = err.get("message", "त्रुटी")
            suggestion = err.get("suggestion", "")
            rule_type = err.get("type", err.get("rule", ""))
            detail = f" → *{suggestion}*" if suggestion else ""
            grammar_lines.append(f"🟡 {message}{detail}")
        sections.append("\n\n".join(grammar_lines))
    else:
        sections.append("✅ व्याकरण बरोबर आहे.")

    return "\n\n".join(sections)


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

    suggestions = data.get("suggestions", [])
    mode = data.get("ranking_mode", "unknown")

    if not suggestions:
        return f"**{word}** साठी सुचवण्या नाहीत. *(mode: {mode})*"

    lines = [f"**{word}** साठी सुचवण्या *(mode: {mode})*:", ""]
    for i, s in enumerate(suggestions, 1):
        lines.append(f"**{i}.** {s}")
    return "\n\n".join(lines)


with gr.Blocks(title="Lekhak — मराठी प्रूफरीडर", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📝 Lekhak — मराठी प्रूफरीडर")
    gr.Markdown("मराठी मजकूर तपासा: शब्दलेखन, व्याकरण आणि सुधारणा सुचवण्या")

    backend_selector = gr.Radio(
        choices=list(BACKENDS.keys()),
        value="Local (localhost:8000)",
        label="🖥️ Backend निवडा"
    )

    with gr.Tab("📄 मजकूर तपासा"):
        text_input = gr.Textbox(
            label="मराठी मजकूर टाका",
            placeholder="उदा. मी मी घरि जातो . आज  छान दिवस आहे.",
            lines=5
        )
        check_btn = gr.Button("✅ तपासा", variant="primary")
        check_output = gr.Markdown(label="निकाल")
        check_btn.click(
            fn=call_check,
            inputs=[text_input, backend_selector],
            outputs=[check_output]
        )

    with gr.Tab("💡 सुचवण्या"):
        word_input = gr.Textbox(label="चुकीचा शब्द", placeholder="उदा. घरि")
        sentence_input = gr.Textbox(
            label="संदर्भ वाक्य (ML ranking साठी, optional)",
            placeholder="उदा. मी घरि जातो"
        )
        ml_toggle = gr.Checkbox(label="MuRIL ML Ranking वापरा (local only)", value=False)
        suggest_btn = gr.Button("💡 सुचवा", variant="primary")
        suggest_output = gr.Markdown(label="सुचवण्या")
        suggest_btn.click(
            fn=call_suggest,
            inputs=[word_input, sentence_input, ml_toggle, backend_selector],
            outputs=[suggest_output]
        )

demo.launch(server_name="0.0.0.0", server_port=7860)
'''

Path("frontend/app.py").write_text(content, encoding="utf-8")
print("frontend/app.py updated — formatting fixed.")    