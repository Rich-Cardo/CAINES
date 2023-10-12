-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 08-10-2023 a las 22:56:23
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `caines`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `aux_facturas`
--

CREATE TABLE `aux_facturas` (
  `id_factura` int(5) NOT NULL,
  `id_terapia` int(5) NOT NULL,
  `cantidad` smallint(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `aux_horarios`
--

CREATE TABLE `aux_horarios` (
  `id_horario` int(5) NOT NULL,
  `id_dia` int(5) NOT NULL,
  `id_especialista` int(5) NOT NULL,
  `id_hora` int(5) NOT NULL,
  `aula` varchar(10) NOT NULL,
  `id_terapia` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `aux_inscripcion`
--

CREATE TABLE `aux_inscripcion` (
  `id_inscripcion` int(5) NOT NULL,
  `id_terapia` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `avances`
--

CREATE TABLE `avances` (
  `id_avance` int(5) NOT NULL,
  `id_especialista` int(5) NOT NULL,
  `id_nino` int(5) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `avances_observaciones`
--

CREATE TABLE `avances_observaciones` (
  `id_avance` int(5) NOT NULL,
  `observaciones` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `avances_recomendaciones`
--

CREATE TABLE `avances_recomendaciones` (
  `id_avance` int(5) NOT NULL,
  `recomendaciones` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `avances_resultados`
--

CREATE TABLE `avances_resultados` (
  `id_avance` int(5) NOT NULL,
  `resultados` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `avance_objetivos`
--

CREATE TABLE `avance_objetivos` (
  `id_avance` int(5) NOT NULL,
  `objetivos` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas`
--

CREATE TABLE `citas` (
  `id_cita` int(5) NOT NULL,
  `id_representante` int(5) NOT NULL,
  `id_niño` int(5) NOT NULL,
  `fecha` date NOT NULL,
  `estado` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas_aprobadas`
--

CREATE TABLE `citas_aprobadas` (
  `id_cita` int(5) NOT NULL,
  `fecha_cita` date NOT NULL,
  `hora_cita` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dias`
--

CREATE TABLE `dias` (
  `id_dia` int(5) NOT NULL,
  `dia` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `facturas`
--

CREATE TABLE `facturas` (
  `id_factura` int(5) NOT NULL,
  `id_usuario` int(5) NOT NULL,
  `descripcion` varchar(40) NOT NULL,
  `pago` varchar(20) NOT NULL,
  `total` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horarios`
--

CREATE TABLE `horarios` (
  `id_horario` int(5) NOT NULL,
  `id_nino` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horas`
--

CREATE TABLE `horas` (
  `id_hora` int(5) NOT NULL,
  `hora_inicio` varchar(40) NOT NULL,
  `hora_fin` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inscripciones`
--

CREATE TABLE `inscripciones` (
  `id_inscripcion` int(5) NOT NULL,
  `fecha_inscripcion` date NOT NULL,
  `id_nino` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ninos`
--

CREATE TABLE `ninos` (
  `id_nino` int(5) NOT NULL,
  `id_usuario` int(5) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `edad` int(3) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `lugar_nacimiento` varchar(20) NOT NULL,
  `num_hermanos` int(2) NOT NULL,
  `escolaridad` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ninos`
--

INSERT INTO `ninos` (`id_nino`, `id_usuario`, `nombre`, `apellido`, `edad`, `fecha_nacimiento`, `lugar_nacimiento`, `num_hermanos`, `escolaridad`) VALUES
(40, 28, 'ds', 'ds', 31, '2023-10-06', 'ds', 0, '2do Grado'),
(41, 28, 'ds', 'dsa', 31, '2023-10-03', 'dsds', 0, '2do Grado'),
(42, 28, 'Nombre', 'apellido', 14, '2023-10-09', 'lugar nac', 0, '3er Grado'),
(43, 28, 'Mi nombre', 'Mi apellido', 5, '2023-10-05', 'Falon', 42, '2do Grado'),
(44, 50, 'Tita', 'Isabela', 3, '2023-10-04', 'guaritos', 0, '3er Grado'),
(45, 51, 'za', 'za', 2, '2023-10-04', 'ds', 0, '2do Grado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `telefonos_usuario`
--

CREATE TABLE `telefonos_usuario` (
  `id_usuario` int(5) NOT NULL,
  `telefono` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `telefonos_usuario`
--

INSERT INTO `telefonos_usuario` (`id_usuario`, `telefono`) VALUES
(16, '04141503936'),
(17, '0412523523523'),
(28, '041231343'),
(31, '0412342131'),
(32, '041242'),
(33, '041211'),
(34, '04123'),
(47, '49023267'),
(49, '19023267'),
(50, '132'),
(51, '19023267');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `terapias`
--

CREATE TABLE `terapias` (
  `id_terapia` int(5) NOT NULL,
  `terapia` varchar(30) NOT NULL,
  `precio` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `terapias`
--

INSERT INTO `terapias` (`id_terapia`, `terapia`, `precio`) VALUES
(2, 'Lenguaje', 15),
(3, 'Psicopedagogia', 20);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(5) NOT NULL,
  `tipo_usuario` varchar(20) NOT NULL,
  `cedula` int(10) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `direccion` varchar(100) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `clave` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `tipo_usuario`, `cedula`, `nombre`, `apellido`, `direccion`, `correo`, `clave`) VALUES
(16, 'representante', 20421842, 'jholbert', 'perez', 'bna', 'qa@gmadt', 'sasa'),
(17, 'representante', 4324234, 'fyhgdg', 'gfdgdg', 'dgddg', 'ghergedgre@a', 'sdf'),
(28, 'especialista', 2020, 'Ricardo', 'Perez', 'a', 'a@aadxzx', 'hg'),
(31, 'administrador', 524, 'Soy Administrador', 'fs', 'fd', 'dsa@sa', 'ds'),
(32, 'secretaria', 14, 'ds', 'ads', 'dsds', 'sda@sa', 'ds'),
(33, 'secretaria', 32, 'Mi Beb', 'Rojas', 'a', 'a@a', 'ds'),
(34, 'director', 10, 'Director', 'dssffdd', 'ds', 'a@sa', 'a'),
(47, 'representante', 29516010, 'Ricardo', 'Perez', 'Los Guaritos III', 'ricardopz126@gmail.com', 'daniel2001.'),
(49, 'representante', 105834, 'sa', 'sa', 'sa', 'ricardopz126@gmail.com', 'sa'),
(50, 'representante', 5050, 'Prueba nombre', 'a', 'a', 'a@a', 'ds'),
(51, 'representante', 80, 'mi', 'mi', 'mi', 'a@a', 'hg');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `aux_facturas`
--
ALTER TABLE `aux_facturas`
  ADD KEY `fk_id_factura` (`id_factura`),
  ADD KEY `fk_id_terapia` (`id_terapia`);

--
-- Indices de la tabla `aux_horarios`
--
ALTER TABLE `aux_horarios`
  ADD KEY `fk_id_horario` (`id_horario`),
  ADD KEY `fk_id_horario_especialista` (`id_especialista`),
  ADD KEY `fk_id_horario_terapia` (`id_terapia`),
  ADD KEY `fk_id_dia` (`id_dia`),
  ADD KEY `fk_id_horario_hora` (`id_hora`);

--
-- Indices de la tabla `aux_inscripcion`
--
ALTER TABLE `aux_inscripcion`
  ADD KEY `fk_terapias` (`id_terapia`),
  ADD KEY `fk_inscripcion` (`id_inscripcion`);

--
-- Indices de la tabla `avances`
--
ALTER TABLE `avances`
  ADD PRIMARY KEY (`id_avance`),
  ADD KEY `fk_id_avance_especialista` (`id_especialista`),
  ADD KEY `fk_id_avance_nino` (`id_nino`);

--
-- Indices de la tabla `avances_observaciones`
--
ALTER TABLE `avances_observaciones`
  ADD KEY `fk_id_avance_observaciones` (`id_avance`);

--
-- Indices de la tabla `avances_recomendaciones`
--
ALTER TABLE `avances_recomendaciones`
  ADD KEY `fk_id_avances_recomendaciones` (`id_avance`);

--
-- Indices de la tabla `avances_resultados`
--
ALTER TABLE `avances_resultados`
  ADD KEY `fk_id_avances_resultados` (`id_avance`);

--
-- Indices de la tabla `avance_objetivos`
--
ALTER TABLE `avance_objetivos`
  ADD KEY `fk_id_avance_objetivos` (`id_avance`);

--
-- Indices de la tabla `citas`
--
ALTER TABLE `citas`
  ADD PRIMARY KEY (`id_cita`),
  ADD KEY `fk_id_nino_cita` (`id_niño`);

--
-- Indices de la tabla `citas_aprobadas`
--
ALTER TABLE `citas_aprobadas`
  ADD KEY `fk_id_cita` (`id_cita`);

--
-- Indices de la tabla `dias`
--
ALTER TABLE `dias`
  ADD PRIMARY KEY (`id_dia`);

--
-- Indices de la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD PRIMARY KEY (`id_factura`),
  ADD KEY `fk_factura` (`id_usuario`);

--
-- Indices de la tabla `horarios`
--
ALTER TABLE `horarios`
  ADD PRIMARY KEY (`id_horario`);

--
-- Indices de la tabla `horas`
--
ALTER TABLE `horas`
  ADD PRIMARY KEY (`id_hora`);

--
-- Indices de la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  ADD PRIMARY KEY (`id_inscripcion`),
  ADD KEY `fk_ninos` (`id_nino`);

--
-- Indices de la tabla `ninos`
--
ALTER TABLE `ninos`
  ADD PRIMARY KEY (`id_nino`),
  ADD KEY `fk_nino_representante` (`id_usuario`);

--
-- Indices de la tabla `telefonos_usuario`
--
ALTER TABLE `telefonos_usuario`
  ADD KEY `fk_telefono_usuario` (`id_usuario`);

--
-- Indices de la tabla `terapias`
--
ALTER TABLE `terapias`
  ADD PRIMARY KEY (`id_terapia`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`,`cedula`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `avances`
--
ALTER TABLE `avances`
  MODIFY `id_avance` int(5) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `citas`
--
ALTER TABLE `citas`
  MODIFY `id_cita` int(5) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `dias`
--
ALTER TABLE `dias`
  MODIFY `id_dia` int(5) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `facturas`
--
ALTER TABLE `facturas`
  MODIFY `id_factura` int(5) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `horarios`
--
ALTER TABLE `horarios`
  MODIFY `id_horario` int(5) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `horas`
--
ALTER TABLE `horas`
  MODIFY `id_hora` int(5) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  MODIFY `id_inscripcion` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `ninos`
--
ALTER TABLE `ninos`
  MODIFY `id_nino` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT de la tabla `terapias`
--
ALTER TABLE `terapias`
  MODIFY `id_terapia` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `aux_facturas`
--
ALTER TABLE `aux_facturas`
  ADD CONSTRAINT `fk_id_factura` FOREIGN KEY (`id_factura`) REFERENCES `facturas` (`id_factura`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_id_terapia` FOREIGN KEY (`id_terapia`) REFERENCES `terapias` (`id_terapia`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `aux_horarios`
--
ALTER TABLE `aux_horarios`
  ADD CONSTRAINT `fk_id_dia` FOREIGN KEY (`id_dia`) REFERENCES `dias` (`id_dia`),
  ADD CONSTRAINT `fk_id_horario` FOREIGN KEY (`id_horario`) REFERENCES `horarios` (`id_horario`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_id_horario_hora` FOREIGN KEY (`id_hora`) REFERENCES `horas` (`id_hora`),
  ADD CONSTRAINT `fk_id_horario_terapia` FOREIGN KEY (`id_terapia`) REFERENCES `terapias` (`id_terapia`);

--
-- Filtros para la tabla `aux_inscripcion`
--
ALTER TABLE `aux_inscripcion`
  ADD CONSTRAINT `fk_inscripcion` FOREIGN KEY (`id_inscripcion`) REFERENCES `inscripciones` (`id_inscripcion`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_terapias` FOREIGN KEY (`id_terapia`) REFERENCES `terapias` (`id_terapia`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `avances`
--
ALTER TABLE `avances`
  ADD CONSTRAINT `fk_id_avance_nino` FOREIGN KEY (`id_nino`) REFERENCES `ninos` (`id_nino`);

--
-- Filtros para la tabla `avances_observaciones`
--
ALTER TABLE `avances_observaciones`
  ADD CONSTRAINT `fk_id_avance_observaciones` FOREIGN KEY (`id_avance`) REFERENCES `avances` (`id_avance`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `avances_recomendaciones`
--
ALTER TABLE `avances_recomendaciones`
  ADD CONSTRAINT `fk_id_avances_recomendaciones` FOREIGN KEY (`id_avance`) REFERENCES `avances` (`id_avance`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `avances_resultados`
--
ALTER TABLE `avances_resultados`
  ADD CONSTRAINT `fk_id_avances_resultados` FOREIGN KEY (`id_avance`) REFERENCES `avances` (`id_avance`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `avance_objetivos`
--
ALTER TABLE `avance_objetivos`
  ADD CONSTRAINT `fk_id_avance_objetivos` FOREIGN KEY (`id_avance`) REFERENCES `avances` (`id_avance`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `citas`
--
ALTER TABLE `citas`
  ADD CONSTRAINT `fk_id_nino_cita` FOREIGN KEY (`id_niño`) REFERENCES `ninos` (`id_nino`);

--
-- Filtros para la tabla `citas_aprobadas`
--
ALTER TABLE `citas_aprobadas`
  ADD CONSTRAINT `fk_id_cita` FOREIGN KEY (`id_cita`) REFERENCES `citas` (`id_cita`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD CONSTRAINT `fk_factura` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  ADD CONSTRAINT `fk_ninos` FOREIGN KEY (`id_nino`) REFERENCES `ninos` (`id_nino`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `ninos`
--
ALTER TABLE `ninos`
  ADD CONSTRAINT `fk_nino_representante` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `telefonos_usuario`
--
ALTER TABLE `telefonos_usuario`
  ADD CONSTRAINT `fk_telefono_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
