import { Languages } from "lucide-react";
import { useI18n, type Language } from "../i18n/I18nContext";

export default function LanguageToggle() {
  const { lang, setLang, t } = useI18n();

  const options: { value: Language; label: string }[] = [
    { value: "zh", label: "中文" },
    { value: "en", label: "EN" },
  ];

  return (
    <div className="flex items-center gap-2">
      <Languages className="w-4 h-4 text-slate-400" />
      <div className="flex bg-slate-800 rounded-lg p-0.5">
        {options.map((opt) => (
          <button
            key={opt.value}
            type="button"
            onClick={() => setLang(opt.value)}
            className={`px-2 py-1 text-xs rounded-md transition-colors ${
              lang === opt.value
                ? "bg-slate-600 text-white"
                : "text-slate-400 hover:text-white"
            }`}
            title={t.app.switchTo}
          >
            {opt.label}
          </button>
        ))}
      </div>
    </div>
  );
}
