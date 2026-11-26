# Phong cách edit Daily Vlog của chị (bắt buộc áp dụng cho mọi vlog sau)

Tài liệu này ghi lại **toàn bộ yêu cầu và sở thích** chị đã chốt khi làm vlog "Sài Gòn – đi giải ngố" (bản chị duyệt: **bản 7 + hiệu ứng đầu to = bản 9**).
Từ nay, mỗi khi edit daily vlog cho chị, làm theo đúng các mục dưới đây. Code và tài nguyên nằm trong `vlog-style/`.

## 0. Cách xưng hô và làm việc
- Gọi **"chị"**, xưng **"em"**. Trả lời ngắn gọn, dễ hiểu, bằng tiếng Việt.
- Chị gửi video bằng **link Google Drive**. Tải bằng `https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t` (network cần cho phép `drive.google.com` và `drive.usercontent.google.com`).
- Gửi chị **bản nhẹ để xem trước**, khi chị ok thì gửi **bản HD để lưu** (khoảng 60–100MB). File 260MB khó tải trên điện thoại.
- **Phải phân tích lời chị nói, hiểu ý và nhấn mạnh đúng ý chị muốn** (chữ to, màu, zoom, âm thanh). Đây là yêu cầu chị nhấn mạnh nhiều lần.

## 1. Quy trình
1. Xem video thô (contact sheet 1 khung/giây), **cắt đoạn trùng lặp**, giữ **góc mặt đẹp**, mục tiêu **2–3 phút**.
2. Viết bài thoại khi chị yêu cầu: **có ý nghĩa, không chỉ kể chuyện**. **Hook gây tò mò** trong 3 giây đầu. **Cuối clip mới hé lộ**, gợi mở "xem clip sau".
3. Chị tự thu âm. Em **chuyển giọng thành chữ** (faster-whisper large-v3, có gợi ý từ riêng), **sửa chữ theo giọng chị**, căn khớp từng từ, rồi **ghép cảnh theo nội dung câu nói** (nói gì thì hiện cảnh đó).
4. Giọng chị **tăng tốc 1,1 lần**, không méo giọng.
5. **Tự kiểm tra lại**: chuyển giọng của video thành phẩm thành chữ, so với phụ đề. Phải khớp (lệch trung bình khoảng 0 giây).

## 2. Hook mở đầu (rất quan trọng)
- Mở bằng **một cảnh gốc hay**, dùng **âm thanh gốc** (vlog này là cảnh vẫy tay "bye bye" ở quán cà phê), dài khoảng 3,7 giây.
- **Hết hook mới vào giọng chị**, bắt đầu bằng "Hello mọi người…". **Không được cắt mất chữ đầu tiên** của ghi âm.
- Tiêu đề hook kiểu **title nổi bật, tách dòng đẹp**: **"BYE BYE"** (Mont XB, xanh pastel, rất to) và *"em đi đây"* (Play It, nghiêng, màu kem). Có ✦ lấp lánh, chữ bật lên lần lượt. **Không cần ghi "đi Sài Gòn".**
- Nếu có người phía sau làm mặt "thái độ" hay biểu cảm hài: dùng **hiệu ứng ĐẦU TO** kiểu CapCut (chỉ phóng to cái đầu khoảng 1,8–1,95 lần, nảy nhẹ, bám theo mặt, người và cảnh giữ nguyên), kèm tiếng **swish + boing**.
- **KHÔNG** zoom cả khung hình vào mặt, và **KHÔNG** thêm nhãn kiểu "ủa, đi thiệt hả?". Chị đã chê bản 8 vì kiểu này.
- Chữ tiêu đề không được che mặt người đang làm hiệu ứng.

## 3. Phụ đề và chữ: phong cách pastel (theo video mẫu chị gửi)
| Thành phần | Font | Màu | Ghi chú |
|---|---|---|---|
| Phụ đề lời thoại | **Mont SB** (Montserrat SemiBold) 56 | trắng, viền tối mờ và blur nhẹ | đơn giản, 4–6 chữ một cụm, không còn chữ lẻ một mình |
| Từ khóa trong phụ đề | như trên | **vàng nhạt** `#FFF1A8` | các ý chính của chị |
| Từ cần nhấn mạnh đặc biệt | như trên, to 125% | **hồng đậm** `#F27B9A` | ví dụ chữ "dở" |
| Tiêu đề chặng | ô số **hồng pastel** (Mont XB) + chữ nghiêng *Play It* màu kem + tiêu đề **Mont XB** in hoa **xanh pastel** `#B4DCF5` + dòng phụ **hồng pastel** `#F4A7C0` | | ví dụ "01 *chặng* CÀ PHÊ & MÁI NGỐ" |
| Nhãn bo tròn (pill) | Mont SB 50, chữ tối | nền trắng / vàng / xanh / hồng pastel | đặt ngay trên phụ đề |
| Chữ nghiêng to để nhấn | *Play It* (Playfair Display Italic) | kem | ví dụ *bật mí*, *kẹt xe*, *đứng hình...*, *clip sau* |
| Lấp lánh | ✦ (DejaVu Sans) | kem | nhấp nháy nhẹ quanh tiêu đề |
- Thanh tiến độ mỏng **màu hồng pastel** ở mép trên.
- Font cũ (Inter Black, chữ vàng viền đen, karaoke tô từng chữ) chị thấy **rập khuôn, không đẹp**. **Không dùng nữa.**
- Luôn xuất kèm file **`.srt`** (lời thoại và chữ nhấn mạnh) cùng **bản không chữ**, để chị tự chỉnh font trong CapCut nếu muốn.

## 4. Nhấn mạnh ý chính (chị yêu cầu từ giờ về sau)
- Nghe kỹ, câu nào là **ý chính hoặc bài học** thì làm nổi bằng: chữ to riêng, màu, **zoom chậm vào** (1,06–1,12 lần), và âm thanh (boom, ding, sparkle).
- Ví dụ chuẩn, câu "những cái em từng **dở** đã không còn **dở** nữa":
  - Lúc nói chữ "dở" đầu: chữ *dở* hồng, to, rung lắc, kèm tiếng boom.
  - Lúc nói "không còn dở": chữ *dở* bị gạch ngang, chữ ***hết dở!*** bật lên, kèm ding và sparkle.
  - Hình zoom vào.
- Câu chủ đề (ví dụ "muốn giỏi thì làm thật nhiều") có tiêu đề chặng riêng và zoom.

## 5. Chuyển cảnh: phải MƯỢT
- Giữa các cảnh: **hòa mờ (dissolve) khoảng 0,3 giây**. Giữa các đoạn lớn: **trượt mượt (smoothleft, up, right, down) khoảng 0,45 giây**, kèm whoosh nhẹ.
- **Không** cắt thẳng thô, **không** zoom giật đầu đoạn. Trong cảnh chỉ lia và zoom chậm nhẹ.
- Màu: saturation 1,12, contrast 1,04, brightness +0,01.

## 6. Âm thanh
- **Giọng chị phải rõ, to, không ồn**: highpass 90, lowpass 12k, afftdn nr=24, EQ (-2,5dB ở 250Hz, +3,5dB ở 3kHz, +1,5dB ở 8kHz), deesser, compressor, gate, gain cố định lên -14 LUFS, limiter.
- Giữ **âm thanh gốc** của clip làm nền: hook để to, khi chị nói thì tự nhỏ lại (sidechain).
- **Hiệu ứng âm thanh theo hành động**, vừa phải, đơn giản:
  - vẫy tay, tạo dáng: swish
  - cầm ly, khoe đồ: sparkle
  - hút ống hút, uống: slurp
  - thắt dây an toàn, cắm sạc: click / zap
  - lắc lư: boing
  - chỉ tay, vẫy chào: pop
  - dang tay khoe: tada
  - múa mì: swish theo nhịp
  - chụp hình: shutter
- Tiếng pop khi hiện chữ chỉ dùng ở chữ quan trọng để không bị ồn. Chưa chèn nhạc nền: chị tự chọn nhạc trend trên TikTok (khoảng 10–15%).

## 7. Xuất file
- 1080×1920, 30fps, H.264. Bản HD gửi chị khoảng `crf 22, maxrate 4M`, kèm hướng dẫn lưu: iPhone vào Tệp → Chia sẻ → Lưu video. Không gửi qua Zalo hay Messenger. Bật Upload HD trên TikTok.

## 8. Tài nguyên trong repo
- `scripts/`: toàn bộ pipeline (render.py, xfade_build.py, mix.py, refstyle.py, …). Chạy với `STYLE=ref HOOK_OFF=<độ dài hook>`.
- `fonts/`: Mont SB, Mont XB, Play It (+ Baloo 2, Pacifico). Copy vào `~/.fonts` rồi chạy `fc-cache -f`.
- `sfx/`: các hiệu ứng âm thanh tự tạo (whoosh, pop, ding, boom, boing, slurp, click, zap, tada, swish, sparkle, shutter, riser).
- `assets/headmask.png`: mặt nạ elip cho hiệu ứng đầu to.
