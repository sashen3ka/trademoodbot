import { useEffect, useState } from "react";
import { db } from "../firebase";
import { collection, getDocs, orderBy, query } from "firebase/firestore";
import { useNavigate } from "react-router-dom";
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

export default function TradeHistory() {
  const [trades, setTrades] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const userId = useUserId();

  useEffect(() => {
    const fetchTrades = async () => {
      try {
        const q = query(collection(db, "users", userId, "trades"), orderBy("timestamp", "desc"));
        const snap = await getDocs(q);
        const data = snap.docs.map((doc) => ({ id: doc.id, ...doc.data() }));
        setTrades(data);
      } catch (e) {
        console.error("Ошибка загрузки сделок:", e);
      } finally {
        setLoading(false);
      }
    };

    fetchTrades();
  }, [userId]);

  if (loading) return <div className="p-4">📂 Загружаем сделки...</div>;

  return (
    <div className="p-4 text-light bg-dark min-h-screen">
      <h2 className="text-2xl font-bold mb-6 text-center text-light">История сделок</h2>
      {trades.length === 0 ? (
        <p className="text-sm text-grayish">Сделок пока нет</p>
      ) : (
        <ul className="space-y-4">
          {trades.map((t) => (
            <li
              key={t.id}
              className="border-b border-zinc-700 pb-4"
            >
              <div className="flex justify-between items-center mb-1">
                <span className="text-grayish text-sm">{formatDate(t.timestamp)}</span>
                <button
                  onClick={() => navigate(`/trade/${t.id}`)}
                  className="text-[#00F7C3] text-sm hover:underline"
                >
                  Посмотреть
                </button>
              </div>
              <div className="flex justify-between font-semibold text-base">
                <span>{t.asset}</span>
                <span className={t.pnl_percent >= 0 ? "text-[#00F7C3]" : "text-red-400"}> 
                  {t.pnl_percent > 0 ? "+" : ""}{t.pnl_percent}% {t.usd_pnl > 0 ? "+" : ""}{t.usd_pnl}$
                </span>
              </div>
              {t.emotion_code && (
                <div className="text-sm mt-1 flex items-center gap-2 text-grayish">
                  <img src={EMOTION_ICONS[t.emotion_code]} alt="emotion" className="w-5 h-5" />
                  <span>{EMOTION_LABELS[t.emotion_code]}</span>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function formatDate(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleDateString("ru-RU", {
    day: "2-digit",
    month: "short",
  });
}
