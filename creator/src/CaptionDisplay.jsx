import React from "react";
import {
  AbsoluteFill,
} from "remotion";
import { CaptionPage } from "./CaptionPage.jsx";

const CaptionDisplay = ({ page }) => {
  // No spring animation - just show the caption directly
  const enterProgress = 1;

  return (
    <AbsoluteFill>
      <CaptionPage enterProgress={enterProgress} page={page} />
    </AbsoluteFill>
  );
};

export default CaptionDisplay;