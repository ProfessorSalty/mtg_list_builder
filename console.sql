DELIMITER $$
DROP FUNCTION IF EXISTS db.IsFoil;
DROP FUNCTION IF EXISTS db.FormatColors;

CREATE FUNCTION db.IsFoil (input text)
RETURNS boolean
DETERMINISTIC
BEGIN
    DECLARE isFoil boolean;
    SET isFoil = input LIKE 'foil';
    RETURN isFoil;
END $$

CREATE FUNCTION db.FormatColors (input text)
RETURNS text
DETERMINISTIC
BEGIN
    DECLARE color text;
    SET color = CASE input
        WHEN 'B' THEN 'Black'
        WHEN 'U' THEN 'Blue'
        WHEN 'R' THEN 'Red'
        WHEN 'G' THEN 'Green'
        WHEN 'W' THEN 'White'
        WHEN 'B,G' THEN 'Golgari'
        WHEN 'R,U' THEN 'Izzet'
        WHEN 'B,R' THEN 'Rekdos'
        WHEN 'B,U' then 'Dimir'
        WHEN 'B,W' THEN 'Orzhsov'
        WHEN 'G,R' THEN 'Gruul'
        WHEN 'G,U' THEN 'Simic'
        WHEN 'G,W' THEN 'Selesnya'
        WHEN 'R,W' THEN 'Boros'
        WHEN 'U,W' THEN 'Zorius'
        WHEN 'B,G,W' THEN 'Abzan'
        WHEN 'G,U,W' THEN 'Bant'
        WHEN 'B,U,W' THEN 'Esper'
        WHEN 'B,R,U' THEN 'Grixis'
        WHEN 'R,U,W' THEN 'Jeskai'
        WHEN 'B,G,R' THEN 'Jund'
        WHEN 'B,R,W' THEN 'Mardu'
        WHEN 'G,R,W' THEN 'Naya'
        WHEN 'B,G,U' THEN 'Sultai'
        WHEN 'G,R,U' THEN 'Temur'
        WHEN 'B,G,R,U' THEN 'Glint'
        WHEN 'B,G,W,R' THEN 'Dune'
        WHEN 'G,U,W,R' THEN 'Ink'
        WHEN 'B,R,U,W' THEN 'Yore'
        WHEN 'B,G,U,W' THEN 'Witch'
        ELSE input
    END;
	RETURN color;
END$$

DELIMITER ;

SELECT
name,
artist,
type as cardType,
FormatColors(colorIdentity) as colorName,
IsFoil(finishes) as isFoil,
colors,
isAlternative,
frameEffects
FROM cards
WHERE setCode = 'ONE' AND isPromo = FALSE
ORDER BY colors, colorName, cardType, name, artist, frameEffects, isFoil;

SELECT name, code, keyruneCode, baseSetSize, type, releaseDate FROM sets WHERE code = 'ONE';


