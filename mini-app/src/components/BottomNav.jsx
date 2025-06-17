import { NavLink, useNavigate } from "react-router-dom";
import icon1 from "../assets/icon1.svg";
import icon2 from "../assets/icon2.svg";
import icon3 from "../assets/icon3.svg";

export default function BottomNav() {
  const navigate = useNavigate();
  const baseClass = "flex flex-col items-center text-xs px-3 pt-2 pb-1 rounded-xl transition";
  const iconClass = "w-6 h-6 mb-1";
  const activeStyle = "bg-[#1a1a1a] text-light font-bold";
  const inactiveStyle = "text-zinc-400 hover:text-white";

  const handleAIChat = () => {
    window.Telegram?.WebApp?.sendData("Обсудить с ИИ 🤖");
    window.Telegram?.WebApp?.close();
  };

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-zinc-900 border-t border-zinc-700 py-2 flex justify-around z-50">
      <button onClick={handleAIChat} className={`${baseClass} ${inactiveStyle}`}>
        <img src={icon1} alt="ИИ" className={iconClass} />
        <span>Обсудить с ИИ</span>
      </button>
      <NavLink to="/add" className={({ isActive }) => `flex flex-col items-center text-xs px-4 pt-3 pb-2 rounded-xl transition bg-[#00997C] text-black font-bold ${isActive ? "opacity-90" : "hover:opacity-100"}`}>
        <img src={icon3} alt="Добавить" className="w-8 h-8 mb-1" />
        <span className="text-sm">Добавить</span>
      </NavLink>
      <NavLink to="/history" className={({ isActive }) => `${baseClass} ${isActive ? activeStyle : inactiveStyle}`}>
        <img src={icon2} alt="История" className={iconClass} />
        <span>История</span>
      </NavLink>
    </div>
  );
}
