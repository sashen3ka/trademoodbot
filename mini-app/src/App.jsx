import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import AddTrade from "./pages/AddTrade";
import Dashboard from "./pages/Dashboard";
import TradeHistory from "./pages/TradeHistory";
import BottomNav from "./components/BottomNav";
import TradeDetails from "./pages/TradeDetails";
import { UserContext } from "./UserContext";

export default function App() {
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    const tg = window.Telegram?.WebApp;
    const user = tg?.initDataUnsafe?.user;
    const initData = tg?.initData;

    if (!initData || !user?.id) {
      alert("⚠️ Пожалуйста, открой Mini App из Telegram.");
      return;
    }

    fetch("https://web-production-40d6f7.up.railway.app/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ initData })
    })
      .then(res => res.json())
      .then(data => {
        if (data.verified && data.userId === user.id.toString()) {
          setUserId(user.id.toString());
          console.log("✅ Telegram user ID подтверждён:", user.id);
        } else {
          alert("❌ Авторизация не прошла.");
        }
      })
      .catch(() => alert("❌ Ошибка при верификации Telegram пользователя"));
  }, []);

  if (!userId) {
    return <div className="p-4 text-center">⏳ Загрузка...</div>;
  }

  return (
    <UserContext.Provider value={userId}>
      <Router>
        <div className="min-h-screen pb-16 text-light" style={{ backgroundColor: "#0A1018" }}>
          <Routes>
            <Route path="/" element={<Navigate to="/stats" />} />
            <Route path="/add" element={<AddTrade />} />
            <Route path="/stats" element={<Dashboard />} />
            <Route path="/history" element={<TradeHistory />} />
            <Route path="/trade/:id" element={<TradeDetails />} />
          </Routes>
          <BottomNav />
        </div>
      </Router>
    </UserContext.Provider>
  );
}
