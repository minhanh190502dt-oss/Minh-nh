# Phong cách edit video — Quán trà sữa MUỐI HOUSE

Áp dụng cho MỌI video về trà sữa / quán Muối House mà chị gửi.
(KHÔNG dùng cho video spa — spa có phong cách riêng, xem `styles/spa.md`.)

Bản mẫu chuẩn: `video-tra-sua-dieu-cay/` (video + script dựng trong `edit-scripts/`).
Muốn làm video mới: copy `edit-scripts/`, chỉ cần sửa `timeline.py` (đoạn cắt, phụ đề, hiệu ứng).

## Định dạng
- Video dọc **9:16, 1080x1920, 30fps**, âm lượng chuẩn TikTok/Reels (-14 LUFS).
- Vibe: vui, Gen Z, nói kiểu miền Tây/miền Nam thân thiện ("mấy bà", "hông", "nha").

## 3 giây đầu (HOOK) — bắt buộc phải thật hút mắt, không được nhạt
- **Video mở đầu NGAY bằng giọng chị** (câu đầu tiên chị nói, vd "Nè nè!") — KHÔNG chèn đoạn teaser im lặng.
  Hiệu ứng hook được đè lên 3 giây đầu trong lúc chị đang nói.
- Chớp trắng + glitch (lệch màu RGB) ngay khung đầu, zoom giật mạnh (1.55x → 1.12x), rung khung.
- Đường tốc độ kiểu anime (focus lines) dồn vào giữa + viền tối (vignette).
- Tiêu đề 2 dòng ĐẬP vào màn hình (scale lớn → nhỏ, kèm "bùm"): dòng 1 trắng, dòng 2 cam có "?!".
- Emoji bung tỏa từ giữa (🧋🔥😱💨).
- **KHÔNG tự bịa chữ quảng cáo/khẳng định về sản phẩm** (vd "HÀNG HIẾM", "BEST SELLER", giá, khuyến mãi…).
  Chữ trên video chỉ lấy từ lời thoại của chị hoặc điều chị yêu cầu. Muốn thêm câu nào ngoài lời thoại thì hỏi chị trước.
- Tiêu đề đặt phía trên (y≈500–710) để không đè phụ đề lời thoại; mờ dần ở giây 2.7–3.0.
- Âm thanh: boom + scratch mở đầu, pop mỗi lần chữ đập, riser dâng dần → drop vào nội dung chính.

## Font & chữ (giống thumbnail kênh Muối House)
- Font: **Grandstander Black (900)** — tròn, mập, kiểu hoạt hình, đủ dấu tiếng Việt.
- Chữ thường: **trắng**, viền **xanh teal đậm** `#094642`.
- Từ khóa nhấn mạnh: **cam** `#FF7A1A`, viền trắng bên trong + viền teal đậm bên ngoài (viền đôi), đổ bóng nhẹ.
- Nhãn/tag: viên thuốc nền **teal** `#146E68` chữ trắng; nhãn kêu gọi comment nền **cam**.
- Phải chừa đủ khoảng trống phía trên để KHÔNG BỊ MẤT DẤU (Ữ, Ế, Ặ, Ố…). Kiểm tra lại khung hình trước khi gửi.

## Phụ đề
- Khớp ĐÚNG lời thoại của chị; câu nào nghe không rõ thì HỎI chị, không tự đoán bừa.
- Hiện theo từng cụm ngắn, nảy lên (pop) khi xuất hiện, đặt khoảng y=1300 (trên vùng nút TikTok).
- Từ khóa viết HOA + tô cam; câu toàn từ khóa thì chữ to hơn và nghiêng nhẹ.
- **Ngắt dòng theo ý nghĩa — KHÔNG BAO GIỜ ngắt ngang xương.** Cụm nhấn mạnh phải nằm trọn
  một dòng, ví dụ: `biểu hiện của` / `SỰ CỐ CHẤP 😤`. Dùng ` | ` trong `timeline.py` để chủ động
  xuống dòng; script không bao giờ tách một cụm tô cam ra 2 dòng.
- Thêm 1 emoji hợp nghĩa cuối câu.
- **Chỉ sub lời thuộc nội dung video.** Câu chị nói với khách/người ngoài (vd "ủa chú ơi",
  "rồi cháu không nghe") thì KHÔNG gắn phụ đề, không thêm hiệu ứng.
- Từ chuyên của quán: "bị complain" = bị khách phàn nàn/phản hồi (không phải "comment").

## Dựng & hiệu ứng
- Cắt bỏ khoảng lặng; mỗi lần cắt xen kẽ zoom 1.0 / 1.07 cho đỡ đều.
- Zoom giật (punch-in) ở câu nhấn mạnh; rung khung + chớp đỏ ở câu "drama" (vd "chắc chết").
- Sticker emoji lắc lư ở góc trên; nhãn chạy ngang kiểu meme ("POV: …", "khách: sao lâu dạ trời").
- Màn kết ~2.6s: nền mờ tối, câu hỏi kêu gọi + nhãn "comment liền cho tui biết nha" + 👇 nhún.

## Âm thanh
- Giọng chị phải RÕ: lọc ồn quán mạnh (afftdn), cắt trầm 100Hz, tăng 3.2kHz (+5dB) cho trong,
  nén giọng, giọng to hơn nhạc rõ rệt.
- Nhạc nền vui tự tạo (không bản quyền), nhỏ (≈0.13) và tự hạ khi chị nói (sidechain).
- SFX: pop, ding, whoosh, boom, scratch, tick đặt ở điểm hài.
