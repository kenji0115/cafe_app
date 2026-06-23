
import streamlit as st
import pandas as pd
import joblib
import altair as alt

# モデル読み込み
pipeline = joblib.load("cafe_pipeline.pkl")
area_mapping = joblib.load("area_mapping.pkl")

# csv読み込み
ratio_df = pd.read_csv("cluster_area_ratio.csv",index_col=0)

# クラスタ名
cluster_names = {
    0: "駅近ランチカフェタイプ",
    1: "大衆向けコンセプトカフェタイプ",
    2: "大人向けコンセプトカフェタイプ",
    3: "郊外ランチカフェタイプ",
    4: "都市部大規模カフェタイプ"
}

# 説明
cluster_descriptions = {
    0: """
    駅近の立地を活かしたランチ営業が中心のカフェタイプ。
    店内Wi-Fiやカード決済に対応している店舗が多く、
    主に利便性を重視する利用者の需要を捉えている。
    子連れ可能だが、ファミリー向けに特化しているわけではない。
    福島・野田や九条・住之江エリアなど準都心エリアに多く見られる。
    """,
    1: """
    子供連れでも利用しやすいサービスを提供するカフェタイプ。
    店内Wi-Fiやカード決済への対応率は低く、
    ランチメニューを提供していない店舗も多い。
    動物カフェやスイーツ専門店なども含まれる。
    高槻・長居エリアなどで比較的多く見られる。
    """,
    2: """
    主に大人向けのサービスを提供するカフェタイプ。
    店内Wi-Fiの対応率が低く、ランチメニューを提供していない店舗も多い。
    子連れ利用をほとんど想定されておらず、コーヒー専門店や、
    アルコールの提供がある店なども含まれる。
    京橋・本町エリアなどで比較的多く見られる。
    """,
    3: """
    車での来店を考慮されている郊外エリアのカフェタイプ。
    店内Wi-Fiの対応率は低いが、ランチメニューを提供している場合が多い。
    ほとんどが駐車場を完備しており、ロードサイド型も多い。
    南河内・泉佐野・枚方エリアなどで比較的多く見られる。
    """,
    4: """
    駅周辺の商業エリアに多い大規模カフェタイプ。
    基本的に毎日営業しており、席数が多い。
    ほとんどがランチメニューを提供しており、
    店内Wi-Fiやカード決済に対応している店舗も多い。
    梅田や心斎橋など都心エリアに多く見られる。
    """
}
# 戦略
cluster_strategy = {
    0: """
    駅利用者やランチ需要の取り込みが期待できる業態です。
    利便性を重視する利用者が多いと考えられるため、
    アクセスの良さや回転率だけでなく、
    Wi-Fi環境や決済手段の充実も重要になります。
    """,

    1: """
    独自のサービスや商品による差別化を図りやすい業態です。
    動物カフェやスイーツ専門店など、コンセプトを明確に打ち出すことで、
    来店動機を作りやすいと考えられます。
    キャッシュレス非対応が多いため、ターゲット層の来店ハードルを
    下げる工夫も検討余地があります。
    """,

    2: """
    特定の趣味や嗜好を持つ利用者を対象とした業態です。
    コンセプトや世界観の一貫性が重要であり、
    ターゲット層を明確に設定することが差別化につながると考えられます。
    SNSや口コミによる情報発信も有効です。
    """,

    3: """
    地域住民や車利用客を主要ターゲットとする業態です。
    駐車場や居心地の良さを活かし、
    長時間滞在やリピート利用を促す工夫が重要になります。
    ランチ需要との相性も良いと考えられます。
    """,

    4: """
    都心部の高需要エリアに適した業態です。
    競合店舗も多いため、席数や利便性だけでなく、
    メニューや空間づくりによる差別化が重要になります。
    幅広い利用目的に対応できる運営が求められます。
    """
}

st.title("大阪カフェ出店タイプ別診断")

st.markdown("""
大阪府全域のカフェ供給データを基に、
エリアごとの店舗傾向や
想定されるカフェタイプを分析します。
""")

st.markdown("## 基本情報")

selected_area = st.selectbox(
    "出店エリア",
    list(area_mapping.keys())
)

capacity = st.slider("席数", 5, 200, 30)

walk_minutes = st.slider("駅から徒歩◯分",1,60,5)

st.markdown("## 設備")

wifi_flag = st.radio(
    "Wi-Fi",
    ["なし", "あり"],
    horizontal=True
)
wifi_flag_num = 1 if wifi_flag == "あり" else 0

card_flag = st.radio(
    "カード決済",
    ["利用不可", "利用可"],
    horizontal=True
)
card_flag_num = 1 if card_flag == "利用可" else 0

parking_flag = st.radio(
    "駐車場",
    ["なし", "あり"],
    horizontal=True    
)
parking_flag_num = 1 if parking_flag == "あり" else 0

st.markdown("## 利用ターゲット")

non_smoking_score = st.radio(
    "禁煙情報",
    ["禁煙席なし", "一部禁煙", "全面禁煙"],
    horizontal=True
)
non_smoking_mapping = {
    "禁煙席なし": 0,
    "一部禁煙": 1,
    "全面禁煙": 2
}

child_flag = st.radio(
    "お子様連れ",
    ["利用不可", "利用可"],
    horizontal=True
)
child_flag_num = 1 if child_flag == "利用可" else 0

st.markdown("## 営業スタイル")

style_weekday_off = st.radio(
    "平日定休日",
    ["なし", "あり"],
    horizontal=True
)
style_weekday_off_num = 1 if style_weekday_off == "あり" else 0

style_weekend_off = st.radio(
    "土日定休日",
    ["なし", "あり"],
    horizontal=True
)
style_weekend_off_num = 1 if style_weekend_off == "あり" else 0

lunch_flag = st.radio(
    "ランチメニュー提供",
    ["なし", "あり"],
    horizontal=True
)
lunch_flag_num = 1 if lunch_flag == "あり" else 0

# エリア変換
area_store_count = area_mapping[selected_area]

# 予測ボタン
if st.button("診断する"):

    new_data = pd.DataFrame([{
        "capacity": capacity,
        "walk_minutes": walk_minutes,
        "area_store_count": area_store_count,
        
        "wifi_flag": wifi_flag_num,
        "card_flag": card_flag_num,
        "parking_flag": parking_flag_num,
        "non_smoking_score": non_smoking_mapping[non_smoking_score],
        "child_flag": child_flag_num,
        
        "style_weekday_off": style_weekday_off_num,
        "style_weekend_off": style_weekend_off_num,
        "lunch_flag": lunch_flag_num
    }])

    cluster = pipeline.predict(new_data)[0]

    st.markdown("## 診断結果")

    st.success(f"あなたの店舗は「{cluster_names[cluster]}」に分類されます。")

    st.info(cluster_descriptions[cluster])

    st.markdown("### 出店戦略ポイント")
    st.write(cluster_strategy[cluster])

    # エリア傾向取得
    area_ratio = ratio_df.loc[selected_area]

    st.subheader("エリア内店舗タイプ傾向")

    display_ratio = area_ratio.copy()

    display_ratio.index = [
        cluster_names[int(i)]
        for i in display_ratio.index
    ]
    chart_df = pd.DataFrame({
    "クラスタ": display_ratio.index,
    "割合": display_ratio.values
    })

    chart = alt.Chart(chart_df).mark_bar().encode(
        x=alt.X("割合:Q",axis=alt.Axis(format="%")),
        y=alt.Y("クラスタ:N",sort="-x")
    ).properties(
        height=300
    ).configure_axisY(
        labelLimit=250
    )

    st.altair_chart(chart, use_container_width=True)


    fit_ratio = area_ratio[str(cluster)]

    st.metric("同タイプ店舗割合",f"{fit_ratio:.0%}")

    if fit_ratio >= 0.35:
        st.success("このエリアで主流となっている店舗タイプです。")
        st.write("""
        既存店舗にも多くみられる業態であり、
        エリア内の供給構造と一致している可能性があります。
        そのため競合店舗が多い可能性が高く、
        競合との差別化も重要になります。
        """)

    elif fit_ratio >= 0.25:
        st.info("このエリアでは一定数見られる店舗タイプです。")
        st.write("""
        既存店舗にも比較的多く見られる業態であり、
        エリア内の供給構造との相性も悪くないと考えられます。
        立地やコンセプト次第で競争力を持てる可能性があります。
        """)
    
    elif fit_ratio >= 0.15:
        st.info("このエリアではややマイナーな店舗タイプです。")
        st.write("""
        既存店舗では比較的少ない業態であり、
        他店舗との差別化につながる可能性があります。
        一方で、エリア需要とのズレには注意が必要です。
        """)

    else:
        st.warning("このエリアでは珍しい店舗タイプです。")
        st.write("""
        既存店舗ではあまり見られない業態のため、
        競合が少ない可能性はあります。
        一方で、同業態の出店情報が少ないため、
        慎重な市場調査が推奨されます。
        """)
