import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { db } from "../firebase";
import { doc, getDoc } from "firebase/firestore";
import { useUserId } from "../UserContext";
import peace from "../assets/peace.svg";
import anxious from "../assets/anxious.svg";
import angry from "../assets/angry.svg";
import confused from "../assets/confused.svg";
import fomo from "../assets/fomo.svg";
import cool from "../assets/cool.svg";

const EMOTION_ICONS = {
  focused_entry: peace,
  doubtful_entry: anxious,
  revenge_mode: angry,
  confused_entry: confused,
  fomo_entry: fomo,
  overconfident: cool,
};

const EMOTION_LABELS = {
  focused_entry: "Спокоен",
  doubtful_entry: "Тревожен",
  revenge_mode: "Отыгрыш",
  confused_entry: "Потерян",
  fomo_entry: "ФОМО",
  overconfident: "Самоуверен",
};

export default function TradeDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const userId = useUserId();
  const [trade, setTrade] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTrade = async () => {
      try {
        const ref = doc(db, "users", userId, "trades", id);
        const snap = await getDoc(ref);
        if (snap.exists()) setTrade(snap.data());
      } catch (e) {
        console.error("Ошибка при загрузке сделки:", e);
      } finally {
        setLoading(false);
      }
    };

    fetchTrade();
  }, [id, userId]);

  const handleDiscuss = () => {
    window.Telegram?.WebApp?.sendData("Обсудить с ИИ 🤖");
    window.Telegram?.WebApp?.close();
  };

  if (loading) return <div className="p-4 text-light bg-dark min-h-screen">🔍 Загрузка...</div>;
  if (!trade) return <div className="p-4 text-light bg-dark min-h-screen">❌ Сделка не найдена</div>;

  return (
    <div className="p-4 text-light bg-dark min-h-screen">
      <h2 className="text-2xl font-bold mb-4">📄 {trade.asset}</h2>

      <div className="text-base space-y-3">
        <div>
          <span className="text-grayish">Результат:</span><br />
          <span className={trade.pnl_percent >= 0 ? "text-[#00F7C3] font-semibold" : "text-red-400 font-semibold"}>
            {trade.pnl_percent > 0 ? "+" : ""}{trade.pnl_percent}%
          </span>
        </div>

        <div>
          <span className="text-grayish">Прибыль:</span><br />
          <span className={trade.usd_pnl >= 0 ? "text-[#00F7C3] font-semibold" : "text-red-400 font-semibold"}>
            {trade.usd_pnl > 0 ? "+" : ""}{trade.usd_pnl}$
          </span>
        </div>

        {trade.emotion_code && (
          <div>
            <span className="text-grayish">Эмоция:</span><br />
            <div className="flex items-center gap-2 mt-1">
              <img src={EMOTION_ICONS[trade.emotion_code]} alt="emotion" className="w-6 h-6" />
              <span>{EMOTION_LABELS[trade.emotion_code]}</span>
            </div>
          </div>
        )}

        {trade.comment && (
          <div>
            <span className="text-grayish">Комментарий:</span><br />
            <span className="text-sm italic">{trade.comment}</span>
          </div>
        )}

        {trade.timestamp && (
          <div>
            <span className="text-grayish">Время:</span><br />
            <span className="text-sm">{new Date(trade.timestamp).toLocaleString()}</span>
          </div>
        )}
      </div>

      <div className="mt-8 flex gap-2">
        <button
          onClick={() => navigate(-1)}
          className="flex-1 bg-zinc-700 py-3 rounded text-light"
        >
          ⬅ Назад
        </button>
        <button
          onClick={handleDiscuss}
          className="flex-1 bg-[#00F7C3] text-black font-bold py-3 rounded"
        >
          Обсудить с ИИ
        </button>
      </div>
    </div>
  );
}
