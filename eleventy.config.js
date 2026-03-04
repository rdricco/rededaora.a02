import { EleventyHtmlBasePlugin } from "@11ty/eleventy";

export default function(eleventyConfig) {
  // Automaticamente conserta links que começam com `/` para incluírem o pathPrefix
  eleventyConfig.addPlugin(EleventyHtmlBasePlugin);

  // Return your Object options:
  return {
    pathPrefix: "/rededaora.a02/",
    dir: {
      input: "src",
      output: "_site"
    }
  }
};
