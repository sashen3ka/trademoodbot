import { useState } from "react";
import EmotionPicker from "../components/EmotionPicker";
import { db } from "../firebase";
import { collection, addDoc } from "firebase/firestore";
import { useUserId } from "../UserContext";

export default function AddTrade() {
  const userId = useUserId();
  const [asset, setAsset] = useState("");
  const [pnlPercent, setPnlPercent] = useState("");
  const [usdPnl, setUsdPnl] = useState("");
  const [emotion, setEmotion] = useState(null);
  const [comment, setComment] = useState("");

  const handleSubmit = async () => {
    const trade = {
      asset,
      pnl_percent: parseFloat(pnlPercent),
      usd_pnl: parseFloat(usdPnl),
      emotion_code: emotion?.code,
      comment: comment || null,
      timestamp: new Date().toISOString(),
      source: "mini_app",
    };
    await addDoc(collection(db, "users", userId, "trades"), trade);
    window.Telegram?.WebApp?.close();
  };

  return (
    <div className="p-4 bg-dark text-light min-h-screen">
      <h2 className="text-xl font-bold mb-6">➕ Новая сделка</h2>

      <div className="mb-4">
        <label className="block text-grayish mb-1">📌 Введи актив (например: BTCUSDT):</label>
        <input
          className="w-full p-2 rounded bg-zinc-800 border border-zinc-600 text-light"
          value={asset}
          onChange={(e) => setAsset(e.target.value)}
          placeholder="BTCUSDT, шорт эфира..."
        />
      </div>

      <div className="mb-4">
        <label className="block text-grayish mb-1">Какой результат в процентах?</label>
        <input
          className="w-full p-2 rounded bg-zinc-800 border border-zinc-600 text-[#00F7C3]"
          value={pnlPercent}
          onChange={(e) => setPnlPercent(e.target.value.replace(",", "."))}
          placeholder="+2.5, -1.2, 0.3"
        />
      </div>

      <div className="mb-4">
        <label className="block text-grayish mb-1">Сколько заработал или потерял в $:</label>
        <input
          className="w-full p-2 rounded bg-zinc-800 border border-zinc-600 text-red-400"
          value={usdPnl}
          onChange={(e) => setUsdPnl(e.target.value.replace(",", "."))}
          placeholder="+100, -85, 0"
        />
      </div>

      <div className="mb-4">
        <label className="block text-grayish mb-2">Эмоция:</label>
        <EmotionPicker selected={emotion} onSelect={setEmotion} />
      </div>

      <div className="mb-6">
        <label className="block text-grayish mb-1">Комментарий:</label>
        <textarea
          className="w-full p-2 rounded bg-zinc-800 border border-zinc-600"
          rows={3}
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="вошёл на автомате, эмоции мешали..."
        />
      </div>

      <button
        onClick={handleSubmit}
        className="w-full bg-[#00F7C3] text-black font-bold py-3 rounded"
      >
        Сохранить
      </button>
    </div>
  );
}
