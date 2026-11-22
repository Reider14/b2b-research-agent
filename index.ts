import { GoogleGenerativeAI, SchemaType, type ResponseSchema } from "@google/generative-ai";
import { z } from "zod";
import * as dotenv from "dotenv";

dotenv.config();


// 1. Definir schema de validacao com zod

const EmpresaSchema = z.object({
    nome: z.string(),
    setor: z.string(),
    tecnologias: z.array(z.string()),
    resumoModeloNegocio: z.string(),
    estimativaFuncionarios: z.number().optional(),
    nivelConfianca: z.enum(["alto", "medio", "baixo"]),
});


const empresaResponseSchema: ResponseSchema = {
    type: SchemaType.OBJECT,
    properties: {
        nome: { type: SchemaType.STRING },
        setor: { type: SchemaType.STRING },
        tecnologias: {
            type: SchemaType.ARRAY,
            items: { type: SchemaType.STRING}, 
        },
        resumoModeloNegocio: {
            type: SchemaType.STRING,
            description: "Resuma o modelo de negocio em no maximo 2 frases",
        },
        estimativaFuncionarios: {
            type: SchemaType.NUMBER,
            description: "Estimativa aproximada. Omite se nao souber."
        },
        nivelConfianca: {
            type: SchemaType.STRING,
            format: "enum",
            enum: ["alto", "medio", "baixo"],
            description: "Nivel de certeza sobre os dados informados.",
        },
        
    },
    required: [
        "nome",
        "setor",
        "tecnologias",
        "resumoModeloNegocio",
        "nivelConfianca",
    ]
}

type Empresa = z.infer<typeof EmpresaSchema>;

async function pesquisarEmpresa(nomeEmpresa: string): Promise<Empresa>{
    const apiKey = process.env["GEMINI_API_KEY"];
    if (!apiKey) {
        throw new Error("GEMINI_API_KEY nao encontrada no .env");
    }

    // 2. Inicializar cliente e modelo em JSON Mode
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({
        model: "gemini-3.8-flash",
        systemInstruction: "Voce e um analista de pesquisa B2B rigoroso. Responda sempre em portugues." 
        + "Nunca invente informacoes: se nao conhecer a empresa ou nao tiver certeza, " 
        + "defina nivelConfianca como 'baixo' e deixe claro no resumo que nao ha dados suficientes.",
        generationConfig: {
            temperature: 0,
            responseMimeType: "application/json",
            responseSchema: empresaResponseSchema,
        },
    });

    const prompt = `Analisa a empresa "${nomeEmpresa}"`;

    //3. Chamar o LLM
    const result = await model.generateContent(prompt);
    const textoBruto = result.response.text();

    //4. Parsear o texto em objeto JS e validar contra o contrato Zod
    const jsonBruto: unknown = JSON.parse(textoBruto);
    const dadosValidados = EmpresaSchema.safeParse(jsonBruto);

    if (!dadosValidados.success) {
        throw new Error("Resposta do LLM nao seguiu o contrato EmpresaSchema.")
    }

    return dadosValidados.data;
}


async function main() {
    for(const empresa of ["Apple", "Kestrel Quantun Logistics", "SpaceX", "Starlink"]){
        console.log(`\nA pesquisar empresa ${empresa}...`);
        const resultado = await pesquisarEmpresa(empresa);
        console.log(resultado);
    }
    
}

main().catch((err) => {
    console.log("Erro na execucao:", err);
    process.exit(1);
})
