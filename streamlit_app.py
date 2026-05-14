import streamlit as st
import mido
import pandas as pd
import plotly.express as px
from io import BytesIO

# 設定頁面
st.set_page_config(page_title="MIDI 演奏視覺化工具", layout="wide")

st.title("🎹 MIDI 自動演奏與視覺化分析")
st.write("上傳您的 `.mid` 檔案，解析其中的複雜節奏與音符分佈。")

# 1. 檔案上傳介面
uploaded_file = st.file_uploader("選擇一個 MIDI 檔案", type=["mid", "midi"])

if uploaded_file is not None:
    # 讀取 MIDI 內容
    midi_data = mido.MidiFile(file=BytesIO(uploaded_file.read()))
    
    st.success(f"成功載入檔案：{uploaded_file.name}")
    
    # 2. 顯示基本資訊 (如您之前提到的 120 BPM 或特殊節奏)
    col1, col2, col3 = st.columns(3)
    col1.metric("總長度 (秒)", f"{round(midi_data.length, 2)}")
    col2.metric("軌道數", len(midi_data.tracks))
    col3.metric("Ticks Per Beat", midi_data.ticks_per_beat)

    # 3. 解析音符數據（用於視覺化）
    notes = []
    current_time = 0
    for msg in midi_data:
        current_time += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            notes.append({
                "Time": current_time,
                "Note": msg.note,
                "Velocity": msg.velocity,
                "Channel": msg.channel
            })

    df = pd.DataFrame(notes)

    # 4. 模擬鋼琴瀑布流 (使用 Plotly 繪圖)
    st.subheader("🎵 音符分佈視覺化 (鋼琴捲軸視角)")
    st.info("這張圖能反映樂譜中的三連音、五連音等複雜對位結構。")
    
    fig = px.scatter(df, x="Time", y="Note", color="Velocity",
                     labels={"Note": "MIDI 音高 (21-108)", "Time": "時間 (秒)"},
                     color_continuous_scale="Viridis",
                     title="音符時序分佈圖")
    
    # 優化圖表外觀，模擬鋼琴範圍
    fig.update_layout(yaxis=dict(range=[21, 108]))
    st.plotly_chart(fig, use_container_width=True)

    # 5. 檔案下載 (讓使用者可以拿回處理過的 MIDI)
    st.download_button(
        label="下載該 MIDI 檔案",
        data=uploaded_file.getvalue(),
        file_name=uploaded_file.name,
        mime="audio/midi"
    )

else:
    st.info("請在左側或上方上傳檔案以開始分析。")
