# Video EZVIZ DL06 (9:16, 1080x1920, 40 giây)

## Các vị trí chèn ảnh thực tế
| Khung | Thời điểm | Vùng ảnh (px trên 1080x1920) | File để render tự động |
|---|---|---|---|
| Ảnh lắp đặt 1 | 0:04.0 – 0:07.5 | x 96–984, y 316–1464 | `anh/slot1.jpg` |
| Ảnh lắp đặt 2 | 0:21.1 – 0:24.6 | x 96–984, y 316–1464 | `anh/slot2.jpg` |
| Ảnh nghiệm thu 1 | 0:31.4 – 0:36.0 | x 90–516, y 400–925 | `anh/nghiemthu1.jpg` |
| Ảnh nghiệm thu 2 | 0:31.4 – 0:36.0 | x 564–990, y 400–925 | `anh/nghiemthu2.jpg` |
| Ảnh nghiệm thu 3 | 0:31.4 – 0:36.0 | x 90–516, y 973–1498 | `anh/nghiemthu3.jpg` |
| Ảnh nghiệm thu 4 | 0:31.4 – 0:36.0 | x 564–990, y 973–1498 | `anh/nghiemthu4.jpg` |
| Liên hệ | 0:37.5 – 0:40.0 | ô gạch đứt cuối video | sửa `contact` trong `video.html` |

Ảnh nghiệm thu nên là ảnh dọc (tỉ lệ khoảng 4:5); ảnh ngang vẫn dùng được, sẽ tự cắt vừa khung.

## Render lại
1. Bỏ ảnh vào `anh/` với đúng tên file ở bảng trên (jpg/png/webp).
2. Sửa chữ trong `CONFIG` ở đầu `video.html` (caption, tiêu đề cảnh nghiệm thu, hotline).
3. `node render.js --preview` để xem trước khung hình (thư mục `preview/`), rồi `python3 make_music.py && node render.js` để xuất `EZVIZ_DL06.mp4`.

Ảnh sản phẩm DL06 + logo: `python3 prep_images.py <thư mục ảnh gốc>` (đã tách nền sẵn trong `anh/`).
