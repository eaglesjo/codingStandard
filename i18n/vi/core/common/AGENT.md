# Quy tắc chung cho AI Agent

1. Đọc và tuân thủ hướng dẫn của repository.
2. Tôn trọng kiến trúc và chính sách hiện có.
3. Kiểm tra code và tests liên quan trước khi thay đổi hành vi.
4. Thêm hoặc cập nhật tests cho thay đổi hành vi.
5. Trừu tượng hóa chi tiết phụ thuộc nền tảng.
6. Không commit secrets hoặc credentials.
7. Chỉ dùng network access khi có yêu cầu rõ ràng.
8. Coi execution environment thực tế là source of truth.
9. Ưu tiên validation có thể tái lập.
10. Chạy validation sau thay đổi và báo cáo kết quả.

## Chu trình thực thi

```text
Inspect → Plan → Change → Validate → Review → Report
```

Kiểm tra memory và runtime trước khi giả định về phần cứng. Với workload dài, xác minh early stopping và checkpoint.