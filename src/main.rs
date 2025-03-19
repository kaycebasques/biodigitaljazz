#[macro_use]
extern crate rocket;

#[cfg(test)]
mod tests;

use image::{ImageBuffer, Rgb};
use rand::prelude::*;
use rocket::Request;
use rocket::http::{ContentType, Header, Status};
use rocket::response::{self, Responder, Response};
use std::io::Cursor;

pub struct NoCache<R>(pub R);

impl<'r, 'o: 'r, R: Responder<'r, 'o>> Responder<'r, 'o> for NoCache<R> {
    fn respond_to(self, req: &'r Request<'_>) -> response::Result<'o> {
        Response::build_from(self.0.respond_to(req)?)
            .header(Header::new(
                "Cache-Control",
                "no-cache, no-store, must-revalidate",
            ))
            .header(Header::new("Pragma", "no-cache"))
            .header(Header::new("Expires", "0"))
            .header(Header::new(
                "Access-Control-Allow-Origin",
                "https://biodigitaljazz.net",
            ))
            .ok()
    }
}

fn generate_favicon() -> Result<Vec<u8>, image::ImageError> {
    let mut rng = rand::rng();
    let mut img = ImageBuffer::new(16, 16);
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
fn get_favicon() -> Result<NoCache<(Status, (ContentType, Vec<u8>))>, Status> {
    match generate_favicon() {
        Ok(image_data) => Ok(NoCache((Status::Ok, (ContentType::Icon, image_data)))),
        Err(_) => Err(Status::InternalServerError),
    }
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![get_favicon])
}
