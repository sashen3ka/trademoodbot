import peace from "../assets/peace.svg";
import anxious from "../assets/anxious.svg";
import angry from "../assets/angry.svg";
import confused from "../assets/confused.svg";
import fomo from "../assets/fomo.svg";
import cool from "../assets/cool.svg";

const EMOTIONS = [
  { code: "focused_entry", icon: peace, label: "Спокойно" },
  { code: "doubtful_entry", icon: anxious, label: "Тревожно" },
  { code: "revenge_mode", icon: angry, label: "Хочу отыграться" },
  { code: "confused_entry", icon: confused, label: "Растерянность" },
  { code: "fomo_entry", icon: fomo, label: "ФОМО" },
  { code: "overconfident", icon: cool, label: "Уверенность" },
];

export default function EmotionPicker({ selected, onSelect }) {
  return (
    <div className="grid grid-cols-2 gap-2 mt-3">
      {EMOTIONS.map((e) => (
        <button
          key={e.code}
          onClick={() => onSelect(e)}
          className={`flex items-center gap-2 py-2 px-3 rounded border text-left ${
            selected?.code === e.code
              ? "bg-white text-black border-white"
              : "bg-zinc-800 border-zinc-600 text-white"
          }`}
        >
          <img src={e.icon} alt={e.label} className="w-5 h-5" />
          <span>{e.label}</span>
        </button>
      ))}
    </div>
  );
}
