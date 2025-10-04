import React from "react";
import {
  AbsoluteFill,
  useVideoConfig,
} from "remotion";
import { BoldFont } from "./load-font.js";
import { fitText } from "@remotion/layout-utils";

const fontFamily = BoldFont;

const container = {
  justifyContent: "center",
  alignItems: "center",
  top: undefined,
  bottom: 350,
  height: 150,
};

const DESIRED_FONT_SIZE = 130;
const FONT_COLOR = "#F7C615"; // Yellow color
const STROKE_COLOR = "black"; // Black border

export const CaptionPage = ({ enterProgress, page }) => {
  const { width } = useVideoConfig();

  const fittedText = fitText({
    fontFamily,
    text: page.text,
    withinWidth: width * 0.9,
    textTransform: "uppercase",
  });

  const fontSize = Math.min(DESIRED_FONT_SIZE, fittedText.fontSize);

  return (
    <AbsoluteFill style={container}>
      <div
        style={{
          fontSize,
          color: FONT_COLOR,
          WebkitTextStroke: `18px ${STROKE_COLOR}`,
          paintOrder: "stroke",
          fontFamily,
          textTransform: "uppercase",
        }}
      >
        <span>
          {page.tokens.map((t) => {
            return (
              <span
                key={t.fromMs}
                style={{
                  display: "inline",
                  whiteSpace: "pre",
                  color: FONT_COLOR, // Yellow color, no highlighting
                }}
              >
                {t.text}
              </span>
            );
          })}
        </span>
      </div>
    </AbsoluteFill>
  );
};