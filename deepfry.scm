; deepfry.scm:
; Description: Creates a "deep-fried" image effect, mostly for memes
; Usage: GIMP script-fu plugin, varies by platform
; Requires: GIMP with script-fu
;
; dev notes:
; this was a difficult one to write because scheme makes me want to scream and
; throw things.
;
; in essence this just adds extreme saturation and sharpening. could probably
; be improved.
;
; just for making dumb memes occasionally, haha.


(define
  (script-fu-deepfry
  img ; image to apply to
  sharpen ; amount to sharpen
  saturate ; amount to saturate)
  )
  (set! drawable (gimp-image-get-active-layer img))
  ; apply saturation
  (plug-in-unsharpen-mask img drawable 3 sharpen 0)
  ; apply sharpening
  (gimp-drawable-hue-saturation drawable 0 0 0 0 sharpen)
  ; flush displays
  (gimp-displays-flush)
)
(script-fu-register
  "script-fu-deepfry" ; name
  "Deep Fry" ; display name
  "Deep fries an image." ; description
  "Brian Lindner" ; author
  "Copyright Brian Lindner, 2018" ; copyright
  "Aug. 13, 2018" ; date
  "RGB*" ; image type
  ; parameters:
  SF-IMAGE "Image"
  SF-ADJUSTMENT "Sharpening" 0 0 50 1 10 1 0 ; Sharpening
  SF-ADJUSTMENT "Saturation" 0 1 10 0.5 1 1 0 ; Saturation
)
(script-fu-menu-register "script-fu-deepfry" "<Filters>/Script-Fu/Deep Fry")
