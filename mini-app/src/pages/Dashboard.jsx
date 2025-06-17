import { useEffect, useState } from "react";
import { db } from "../firebase";
import { collection, getDocs } from "firebase/firestore";
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  ArcElement,
} from "chart.js";
import { Line, Pie } from "react-chartjs-2";
import { useUserId } from "../UserContext";

ChartJS.register(LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend, ArcElement);

export default function Dashboard() {
  const [trades, setTrades] = useState([]);
  const userId = useUserId();

  useEffect(() => {
    const fetchTrades = async () => {
      const snap = await getDocs(collection(db, "users", userId, "trades"));
      const data = snap.docs.map((doc) => doc.data());
      setTrades(data);
    };
    fetchTrades();
  }, [userId]);

  const grouped = {};
  const emotions = {};
  let totalProfit = 0;
  let success = 0;
  let fail = 0;
  let neutral = 0;

  trades.forEach((t) => {
    const dateKey = new Date(t.timestamp).toISOString().split("T")[0];
    grouped[dateKey] = (grouped[dateKey] || 0) + (t.usd_pnl || 0);
    emotions[t.emotion_code] = (emotions[t.emotion_code] || 0) + 1;

    if ((t.pnl_percent || 0) > 0) success++;
    else if ((t.pnl_percent || 0) < 0) fail++;
    else neutral++;

    totalProfit += t.usd_pnl || 0;
  });

  const sortedDates = Object.keys(grouped).sort((a, b) => new Date(a) - new Date(b));
  const displayLabels = sortedDates.map((key) =>
    new Date(key).toLocaleDateString("ru-RU", { day: "2-digit", month: "short" })
  );

  const lineData = {
    labels: displayLabels,
    datasets: [
      {
        label: "",
        data: sortedDates.map((key) => grouped[key]),
        borderColor: "#00f7c3",
        backgroundColor: "transparent",
        tension: 0.4,
        borderWidth: 3,
        pointRadius: 2,
      },
    ],
  };

  const lineOptions = {
    responsive: true,
    plugins: {
      legend: { display: false },
    },
    scales: {
      x: {
        ticks: { color: "#9BA5B2" },
        grid: { color: "#1a1f2a" },
      },
      y: {
        ticks: { color: "#9BA5B2" },
        grid: { color: "#1a1f2a" },
      },
    },
  };

  const pieData = {
    labels: ["Успешные", "Убыточные", "Нейтральные"],
    datasets: [
      {
        data: [success, fail, neutral],
        backgroundColor: ["#16A34A", "#DC2626", "#6B7280"],
        borderWidth: 0,
      },
    ],
  };

  const pieOptions = {
    plugins: {
      legend: { display: false },
    },
  };

  const phrases = [
    "Ты не обязан быть идеальным, чтобы быть прибыльным",
    "Твоя задача — не предсказать рынок, а следовать стратегии",
    "Дисциплина важнее вдохновения",
    "Одна сделка ничего не решает. Главное — серия",
    "Сохраняй спокойствие и торгуй по плану",
    "Прибыль приходит к тем, кто не сдается",
    "Лучше упустить сделку, чем войти на эмоциях",
    "Твоя сила — в последовательности",
    "Неудача — часть пути к успеху",
    "Меньше шума, больше системы",
    "Сомневаешься — не входи",
    "Психология сильнее анализа"
  ];

  const phrase = phrases[new Date().getDate() % phrases.length];

  if (trades.length === 0) {
    return (
      <div className="p-4 bg-dark text-light min-h-screen flex items-center justify-center">
        <p className="text-grayish text-center">Нет данных для отображения. Добавь первую сделку, чтобы увидеть статистику.</p>
      </div>
    );
  }

  return (
    <div className="p-4 bg-dark text-light min-h-screen">
      <h2 className="text-xl font-bold mb-4 text-center">📈 Главная</h2>

      <div className="mb-8">
        <div className="flex justify-between items-center mb-2">
          <h3 className="text-sm text-grayish text-center w-full">Динамика прибыли по дням</h3>
          <button className="absolute right-4 top-16 bg-zinc-800 text-grayish text-xs px-3 py-1 rounded-full border border-zinc-600">Неделя</button>
        </div>
        <Line data={lineData} options={lineOptions} />
      </div>

      <div className="mb-8 flex items-center gap-4">
        <div className="w-1/2">
          <Pie data={pieData} options={pieOptions} />
        </div>
        <div className="text-sm space-y-2">
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-[#16A34A]"></span> <span className="text-grayish">Успешные</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-[#DC2626]"></span> <span className="text-grayish">Убыточные</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-[#6B7280]"></span> <span className="text-grayish">Нейтральные</span>
          </div>
        </div>
      </div>

      <div className="text-center text-grayish text-sm italic mt-8">
        {phrase}
      </div>
    </div>
  );
}
