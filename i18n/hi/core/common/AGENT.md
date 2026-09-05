# AI एजेंट के लिए सामान्य नियम

1. रिपॉजिटरी के निर्देशों को पहले पढ़ें और उनका पालन करें।
2. मौजूदा आर्किटेक्चर और नीति की सीमाओं का सम्मान करें।
3. बदलाव से पहले संबंधित कोड और tests का संदर्भ देखें।
4. व्यवहार में बदलाव होने पर उपयुक्त tests जोड़ें या अपडेट करें।
5. platform-specific विवरणों को उचित abstraction के पीछे रखें।
6. secrets या credentials को commit न करें।
7. network access केवल स्पष्ट आवश्यकता होने पर उपयोग करें।
8. वास्तविक execution environment को source of truth मानें।
9. reproducible validation को प्राथमिकता दें।
10. बदलाव के बाद validation चलाएँ और परिणाम दर्ज करें।

## Execution cycle

```text
Inspect → Plan → Change → Validate → Review → Report
```

Environment, memory और runtime क्षमता को मापे बिना hardware assumptions न करें। बड़े workload में early stopping और checkpoint व्यवहार को भी सत्यापित करें।
