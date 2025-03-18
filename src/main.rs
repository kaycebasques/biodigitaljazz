#[macro_use]
extern crate rocket;

#[cfg(test)]
mod tests;

use image::{ImageBuffer, Rgb};
use rand::prelude::*;
use rocket::http::{ContentType, Status};
use std::io::Cursor;

// fn generate_random_image() -> ImageBuffer<Rgb<u8>, Vec<u8>> {
//     let mut rng = rand::rng();
//
//     // Create a new RGB image buffer
//     let mut img = ImageBuffer::new(FAVICON_SIZE, FAVICON_SIZE);
//
//     // Fill with random RGB values
//     for x in 0..FAVICON_SIZE {
//         for y in 0..FAVICON_SIZE {
//             let r: u8 = rng.random::<u8>();
//             let g: u8 = rng.random::<u8>();
//             let b: u8 = rng.random::<u8>();
//             img.put_pixel(x, y, Rgb([r, g, b]));
//         }
//     }
//
//     img
// }

fn generate_favicon() -> Result<Vec<u8>, image::ImageError> {
    let mut rng = rand::rng();
    let mut img = ImageBuffer::new(100, 100);
    for (_, _, pixel) in img.enumerate_pixels_mut() {
        let r: u8 = rng.random::<u8>();
        let g: u8 = rng.random::<u8>();
        let b: u8 = rng.random::<u8>();
        *pixel = Rgb([r, g, b]);
    }
    let mut buffer = Cursor::new(Vec::new());
    img.write_to(&mut buffer, image::ImageFormat::Ico)?;
    Ok(buffer.into_inner())
}

#[get("/favicon.ico")]
fn get_favicon() -> (Status, (ContentType, Vec<u8>)) {
    match generate_favicon() {
        Ok(image_data) => (Status::Ok, (ContentType::Icon, image_data)),
        Err(_) => (
            Status::InternalServerError,
            (ContentType::Text, "Image generation failed".into()),
        ),
    }
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![get_favicon])
}

// use image::codecs::ico::IcoEncoder;
// use image::{ImageBuffer, Rgb};
// use rocket::http::{ContentType, Status};
// use rocket::response::status;
// use rocket::{get, routes};
// use std::io::Cursor;
//
// // Define a favicon size
// const FAVICON_SIZE: u32 = 16;
//
// #[get("/favicon.ico")]
// fn favicon() -> status::Accepted<ImageBuffer<Rgb<u8>, Vec<u8>>> {
//     let image_buffer = generate_random_image();
//     let mut ico_data = Vec::new();
//     let encoder = IcoEncoder::new(&mut ico_data);
//     match image_buffer.write_with_encoder(encoder) {
//         Ok(_) => {
//             // Return the image as a response
//             Response::build()
//                 .header(ContentType::Icon)
//                 .sized_body(ico_data.len(), Cursor::new(ico_data))
//                 .status(Status::Ok)
//                 .finalize()
//         }
//         Err(_) => {
//             // Return a 500 error if encoding fails
//             Response::build()
//                 .status(Status::InternalServerError)
//                 .finalize()
//         }
//     }
// }
//
